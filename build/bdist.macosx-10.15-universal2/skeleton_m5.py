import cv2
import mediapipe as mp
import numpy as np
import time  # <-- यह अब जोड़ दिया गया है

# MediaPipe के नए Tasks API का इस्तेमाल
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 1. मॉडल सेटअप
base_options = python.BaseOptions(model_asset_path='pose_landmarker.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO)

cap = cv2.VideoCapture(0)

# Skeleton की लाइनों के कनेक्शन (हड्डियों का ढांचा जोड़ने के लिए)
POSE_CONNECTIONS = [
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
    (11, 23), (12, 24), (23, 24), (23, 25), (24, 26), (25, 27), (26, 28)
]

print("M4 Privacy Mode: ON (Skeleton Only). Press 'q' to quit.")

with vision.PoseLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        # काली स्क्रीन बनाना (image_32.png जैसा लुक)
        black_screen = np.zeros(frame.shape, dtype=np.uint8)
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        frame_timestamp_ms = int(time.time() * 1000)
        
        # पोज़ डिटेक्ट करना
        results = landmarker.detect_for_video(mp_image, frame_timestamp_ms)

        if results.pose_landmarks:
            for landmarks in results.pose_landmarks:
                # डॉट्स (Landmarks) बनाना
                for landmark in landmarks:
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    cv2.circle(black_screen, (x, y), 3, (0, 255, 0), -1)

                # हड्डियां (Connections) जोड़ना
                for connection in POSE_CONNECTIONS:
                    start_point = landmarks[connection[0]]
                    end_point = landmarks[connection[1]]
                    
                    start_x = int(start_point.x * frame.shape[1])
                    start_y = int(start_point.y * frame.shape[0])
                    end_x = int(end_point.x * frame.shape[1])
                    end_y = int(end_point.y * frame.shape[0])
                    
                    cv2.line(black_screen, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

        cv2.imshow('Rajnish AI Guard - M4 Skeleton View', black_screen)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()