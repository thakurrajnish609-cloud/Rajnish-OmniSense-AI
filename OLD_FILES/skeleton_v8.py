import cv2
import numpy as np
import mediapipe as mp

# MediaPipe Pose और Drawing Utilities को लोड करना
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

print("--- WiFi CSI Style Sensing Active ---")
print("Status: Privacy Screen ON (Camera Hidden)")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # 1. 'Black Screen' बनाना (Camera feed को पूरी तरह छुपाने के लिए)
    black_screen = np.zeros(frame.shape, dtype=np.uint8)

    # 2. Frame को RGB में बदलना (MediaPipe के लिए ज़रूरी)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose_tracker.process(rgb_frame)

    # 3. सिर्फ Skeleton को काली स्क्रीन पर ड्रा करना
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            black_screen, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2), # ग्रीन जॉइंट्स
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2) # सफेद हड्डियां
        )
        
        # स्टेटस अपडेट
        cv2.putText(black_screen, "SENSING HUMAN MOTION", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # 4. आउटपुट दिखाना (इसमें आपका चेहरा नहीं दिखेगा)
    cv2.imshow('Skeleton Security Monitor', black_screen)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()