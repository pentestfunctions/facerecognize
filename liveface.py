import cv2
import dlib
import numpy as np
import os
import sys
import tkinter as tk
from threading import Thread
import urllib.request

# URL of the shape predictor model
shape_predictor_url = 'https://github.com/italojs/facial-landmarks-recognition/raw/master/shape_predictor_68_face_landmarks.dat'
shape_predictor_path = 'shape_predictor_68_face_landmarks.dat'

# Check if the shape_predictor file exists, and if not, download it
if not os.path.isfile(shape_predictor_path):
    print(f"Downloading shape predictor from: {shape_predictor_url}")
    urllib.request.urlretrieve(shape_predictor_url, shape_predictor_path)
    print("Download complete.")

# Function to check available cameras
def check_cameras(max_check=10):
    available_cameras = []
    for i in range(max_check):
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:
            available_cameras.append(i)
            cap.release()
    return available_cameras

# Function to clear the console screen
def clear_screen():
    if os.name == 'nt':  # Windows
        _ = os.system('cls')
    else:  # macOS and Linux
        _ = os.system('clear')

# List available cameras
available_cameras = check_cameras()
if not available_cameras:
    print("No cameras found.")
    sys.exit()

# Prompt user to select a camera
clear_screen()
print("Available cameras:")
for index, camera in enumerate(available_cameras):
    print(f"{index}: Camera {camera}")
camera_index = int(input("Select camera number: "))
if camera_index not in range(len(available_cameras)):
    print("Invalid camera number.")
    sys.exit()
    
# Helper functions
def draw_rectangle(frame, face):
    x1, y1 = face.left(), face.top()
    x2, y2 = face.right(), face.bottom()
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

def draw_dots(frame, landmarks):
    for n in range(landmarks.num_parts):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

# Define a function to draw lines between landmarks
def draw_polyline(frame, landmarks, points, is_closed=False):
    pts = np.array([(landmarks.part(point).x, landmarks.part(point).y) for point in points], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], is_closed, (255, 255, 255), 1)

# Facial landmark's indices for each part
JAWLINE_POINTS = list(range(0, 17))
RIGHT_EYEBROW_POINTS = list(range(17, 22))
LEFT_EYEBROW_POINTS = list(range(22, 27))
NOSE_BRIDGE_POINTS = list(range(27, 31))
LOWER_NOSE_POINTS = list(range(30, 36))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
OUTER_LIP_POINTS = list(range(48, 60))
INNER_LIP_POINTS = list(range(60, 68))

# Helper function to draw all segments
def draw_landmarks(frame, landmarks, draw_lines=False):
    if draw_lines:
        draw_polyline(frame, landmarks, JAWLINE_POINTS)
        draw_polyline(frame, landmarks, RIGHT_EYEBROW_POINTS)
        draw_polyline(frame, landmarks, LEFT_EYEBROW_POINTS)
        draw_polyline(frame, landmarks, NOSE_BRIDGE_POINTS)
        draw_polyline(frame, landmarks, LOWER_NOSE_POINTS, is_closed=True)
        draw_polyline(frame, landmarks, RIGHT_EYE_POINTS, is_closed=True)
        draw_polyline(frame, landmarks, LEFT_EYE_POINTS, is_closed=True)
        draw_polyline(frame, landmarks, OUTER_LIP_POINTS, is_closed=True)
        draw_polyline(frame, landmarks, INNER_LIP_POINTS, is_closed=True)

# Initialize global variables for draw modes
draw_mode = {'box': False, 'dots': False, 'lines': False}

# Define a function to update draw modes based on GUI
def update_draw_mode(mode, value):
    global draw_mode
    draw_mode[mode] = value

# Define the GUI in a function
def run_gui():
    def toggle_mode(mode):
        current_value = draw_mode[mode]
        update_draw_mode(mode, not current_value)
        buttons[mode].config(relief="sunken" if not current_value else "raised")

    root = tk.Tk()
    root.title("Mode Toggler")

    buttons = {
        'box': tk.Button(root, text="Box", width=10, command=lambda: toggle_mode('box')),
        'dots': tk.Button(root, text="Dots", width=10, command=lambda: toggle_mode('dots')),
        'lines': tk.Button(root, text="Lines", width=10, command=lambda: toggle_mode('lines'))
    }

    for button in buttons.values():
        button.pack(pady=5)

    # Start the GUI
    root.mainloop()

# Start the GUI in a separate thread
gui_thread = Thread(target=run_gui, daemon=True)
gui_thread.start()

# Create a face detector and a landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(available_cameras[camera_index])

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Create a named window
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

# Resize the window to the desired dimensions (e.g., 800x600)
cv2.resizeWindow('frame', 1280, 720)

while True:
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:
        print("Failed to grab frame")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale

    # Detect faces in the grayscale frame
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # Draw based on the current draw mode
        if draw_mode['box']:
            draw_rectangle(frame, face)
        if draw_mode['dots']:
            draw_dots(frame, landmarks)
        if draw_mode['lines']:
            draw_landmarks(frame, landmarks, draw_lines=True)

    cv2.imshow('frame', frame)  # Display the frame in a window

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit the loop if the 'q' key is pressed
        break

cap.release()  # Release the VideoCapture object
cv2.destroyAllWindows()  # Close all OpenCV windows
# No need to close the Tkinter window as it will close with the program
