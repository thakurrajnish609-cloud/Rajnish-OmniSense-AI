import cv2
import numpy as np
try:
    import mediapipe as mp
    from mediapipe.python.solutions import pose as mp_pose
    from mediapipe.python.solutions import drawing_utils as mp_drawing
except ImportError:
    print("Error: MediaPipe not found. Run 'pip install mediapipe'")

# Pose सेटअप
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

print("OmniSense Privacy Shield: ACTIVE")

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
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2)
        )
        
        cv2.putText(black_screen, "SENSING MOTION BEHIND WALL", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # चेहरा छुपाने के लिए सिर्फ काली स्क्रीन और लाइन्स दिखाएं
    cv2.imshow('Privacy View (No Camera Feed)', black_screen)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()