# HAND DETECTION 


Hardware Requirements:

    Camera
    Nvidia Jetson Nano

Software Requirements:

    Python 3
    OpenCV
    MediaPipe (Python Library)

Steps:
Step 1: Frame Capture

Capture images from the USB camera using OpenCV. This will allow you to grab each frame for processing.
Step 2: Algorithm

Once the image is captured, pass the frame to MediaPipe for analysis. If a hand is detected within the region of interest (ROI), display a text overlay on the live video feed indicating the detection.
