import cv2
import numpy as np
import mediapipe as mp

# Direct Import for compatibility (cite: User Summary)
from mediapipe.python.solutions import pose as mp_pose
from mediapipe.python.solutions import drawing_utils as mp_drawing

# Initialize Pose AI
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0) # 0 for default, 1 for MacBook Camera (cite: User Summary)

print("OmniSense Radar Core: Security Mode Active")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # Pure Black Background for Security/Privacy (cite: User Summary)
    h, w, _ = frame.shape
    black_screen = np.zeros((h, w, 3), dtype=np.uint8)

    # AI Processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # Drawing like image_42.png (cite: image_42.png)
        mp_drawing.draw_landmarks(
            black_screen, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            # Dots: Bright Green & Bold
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=-1, circle_radius=6), 
            # Lines: Slim Green
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
        )
        
        # Security Overlay
        cv2.putText(black_screen, "RADAR: MOTION DETECTED", (30, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow('OmniSense Security Monitor', black_screen)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()