import cv2
import mediapipe as mp
import numpy as np

# MediaPipe Pose सेटअप
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

print("Wall Sensing Mode: Active. Privacy Screen: ON")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # 1. काली स्क्रीन बनाना (यही 'Wall' का काम करेगी)
    black_screen = np.zeros(frame.shape, dtype=np.uint8)

    # 2. पोज़ डिटेक्ट करना
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    # 3. सिर्फ 'Skeleton' को काली स्क्रीन पर ड्रा करना
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            black_screen, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2), # डॉट्स
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2) # सफेद लाइनें
        )
        
        # हलचल का पता लगाने के लिए टेक्स्ट
        cv2.putText(black_screen, "MOTION DETECTED BEHIND WALL", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # आउटपुट दिखाएं (इसमें आपका चेहरा नहीं दिखेगा)
    cv2.imshow('OmniSense Privacy View', black_screen)
    
    if cv2.waitKey(10) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()