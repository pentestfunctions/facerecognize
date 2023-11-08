# Facial Landmark Detection

This Python script utilizes OpenCV and Dlib to perform facial landmark detection on video from a webcam. Users can toggle the display of bounding boxes, facial landmark dots, and lines connecting landmarks in real-time using a simple Tkinter GUI.

## How It Works

The script performs the following steps:

1. Checks for available cameras on the system.
2. Downloads a pre-trained Dlib facial landmark detection model if not present.
3. Initializes a Tkinter GUI for toggling the display of boxes, dots, and lines on detected faces.
4. Opens a selected camera using OpenCV and begins capturing video.
5. Converts the video frames to grayscale for facial detection.
6. Uses the Dlib detector to find faces and the predictor to locate facial landmarks.
7. Draws the desired facial landmark visualization on the frame.
8. Displays the video with an overlay of facial landmarks in real-time.
9. Allows the user to exit the program by pressing 'q'.

## Installation

To use this script, you will need Python installed on your system, as well as the following Python libraries:
- `opencv-python`
- `dlib`
- `numpy`
- `tkinter`

```bash
git clone https://github.com/pentestfunctions/facerecognize.git
cd facerecognize
pip install -r requirements.txt
python liveface.py
```


You can install the necessary libraries using `pip`:

```bash
pip install opencv-python dlib numpy
```
Note: Tkinter comes pre-installed with Python.

## Usage

Run the script in a terminal or command prompt:

```bash
python facial_landmark_detection.py
```

Use the Tkinter GUI to toggle the display modes for the detection:

- Click "Box" to toggle the display of bounding boxes around detected faces.
- Click "Dots" to toggle the display of facial landmark dots.
- Click "Lines" to toggle the display of lines connecting facial landmarks.
- To quit the application, focus on the video window and press the 'q' key.

## Setting Up a Virtual Camera with OBS

To output the facial landmark detection to a virtual camera that can be used in video calls, streaming, or any application that accepts a camera input, follow these steps:

1. Download and install OBS Studio from the official website.
2. Open OBS Studio and create a new scene.
3. Add a new source by clicking the '+' button in the Sources panel and select 'Window Capture'.
4. Choose the window that displays the facial landmark detection (the 'frame' window from the script).
5. Resize and adjust the source as needed to fit the canvas.
6. Go to 'Tools' > 'VirtualCam' in the OBS menu bar.
7. Click on 'Start' to start the virtual camera output, choose the capture screen.
8. In your video call or streaming application, select the OBS virtual camera as your camera source.
9. Now you should see the facial landmark detection overlay in your chosen application.
