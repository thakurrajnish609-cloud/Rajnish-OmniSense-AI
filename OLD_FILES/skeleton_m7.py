import cv2
import numpy as np
import mediapipe as mp

# पोज़ डिटेक्शन सेटअप
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

print("Skeleton Privacy Mode: Starting...")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # काली स्क्रीन बनाना (सिर्फ इंसान की लाइनें दिखाने के लिए)
    black_screen = np.zeros(frame.shape, dtype=np.uint8)

    # पोज़ को प्रोसेस करना
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    # अगर इंसान मिलता है तो स्केलेटन ड्रॉ करें
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            black_screen, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2), # डॉट्स
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2) # सफेद लाइनें
        )

    cv2.imshow('OmniSense Skeleton View', black_screen)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()