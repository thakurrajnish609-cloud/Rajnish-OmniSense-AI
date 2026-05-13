import cv2
import numpy as np
import sys

# प्राइवेसी के लिए: सीधा 'Path' आधारित इम्पोर्ट
try:
    import mediapipe.python.solutions.pose as mp_pose
    import mediapipe.python.solutions.drawing_utils as mp_drawing
except Exception as e:
    print(f"Bypass Error: {e}")
    print("कोशिश करें: pip install mediapipe")
    sys.exit()

# पोज़ डिटेक्शन सेटअप (M4 Chip Optimized)
pose_tracker = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

print("--- WiFi CSI Style Sensing Active ---")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # काली स्क्रीन (सिर्फ सुरक्षा के लिए)
    black_screen = np.zeros(frame.shape, dtype=np.uint8)

    # प्रोसेसिंग
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose_tracker.process(rgb_frame)

    # स्केलेटन ड्रा करना
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            black_screen, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2)
        )
        cv2.putText(black_screen, "HUMAN MOTION DETECTED", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('Skeleton Security Monitor', black_screen)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()