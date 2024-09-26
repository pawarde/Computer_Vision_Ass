import cv2
import mediapipe as mp
import time
import os
# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Drawing utility from MediaPipe for drawing hand landmarks
mp_draw = mp.solutions.drawing_utils

# Define the coordinates for the ROI (Region of Interest)
x_start, y_start, x_end, y_end = 100, 100, 600, 400  # Example ROI coordinates
currentdirpath=os.getcwd()
# Open laptop camera (0 is usually the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open the video device")
    exit()
# Set the video frame width and height (Increase the resolution here)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width to 1280 pixels
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set height to 720 pixels (HD resolution)

while True:
    try:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Draw the ROI rectangle
        cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

        # Crop the frame to the ROI
        roi = frame[y_start:y_end, x_start:x_end]

        # Convert the ROI to RGB for MediaPipe (MediaPipe requires RGB format)
        roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

        # Use MediaPipe Hands to detect hands in the ROI
        result = hands.process(roi_rgb)

        # Check if hands were detected
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Get the pixel coordinates of the first landmark (landmark 0)
                h, w, _ = roi.shape
                first_landmark = hand_landmarks.landmark[0]
                cx, cy = int(first_landmark.x * w), int(first_landmark.y * h)

                # Adjust coordinates relative to the full frame
                cx += x_start
                cy += y_start

                # Add the label "Hand" just above the detected hand (above the first landmark)
                cv2.putText(frame, "Hand", (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Draw the hand landmarks on the original frame (not only the ROI)
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
        # Display the frame with hand detection
        cv2.imshow("Hand Detection in ROI", frame)

        # when press s then save image
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(f"HAND_DETET{str(int(time.time()*1000))}.jpg",frame)
            

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        print(e)
# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
