import cv2
import numpy as np

# प्राइवेसी के लिए: सीधा इम्पोर्ट तरीका
try:
    from mediapipe.python.solutions import pose as mp_pose
    from mediapipe.python.solutions import drawing_utils as mp_drawing
except Exception as e:
    # अगर ऊपर वाला फेल हो तो ये दूसरा तरीका
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

# पोज़ ट्रैकर सेटअप
pose_tracker = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

print("--- OMNISENSE SKELETON MODE: ACTIVE ---")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # 1. काली स्क्रीन (Wall-Sensing Simulation)
    # इसमें चेहरा नहीं दिखेगा, सिर्फ ढांचा दिखेगा
    black_screen = np.zeros(frame.shape, dtype=np.uint8)

    # 2. प्रोसेसिंग
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose_tracker.process(rgb_frame)

    # 3. सिर्फ Skeleton ड्रा करना
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            black_screen, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2), # जॉइंट्स
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2) # हड्डियां
        )
        cv2.putText(black_screen, "HUMAN DETECTED", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('OmniSense Skeleton Monitor', black_screen)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()