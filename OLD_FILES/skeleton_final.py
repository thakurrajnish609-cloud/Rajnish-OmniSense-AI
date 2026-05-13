import cv2
import numpy as np
import mediapipe as mp

# पोज़ डिटेक्शन के लिए सही मॉड्यूल लोड करना
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# पोज़ ट्रैकर सेटअप (M4 चिप के लिए ऑप्टिमाइज़्ड)
pose_tracker = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1, 
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

print("--- WiFi CSI Style Sensing: ONLINE ---")
print("Press 'q' to stop safely.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # 1. काली स्क्रीन बनाना (यही आपकी सुरक्षा की दीवार है)
    black_screen = np.zeros(frame.shape, dtype=np.uint8)

    # 2. प्रोसेसिंग (BGR को RGB में बदलना)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose_tracker.process(rgb_frame)

    # 3. सिर्फ स्केलेटन ड्रा करना (इंसान को ट्रैक करने के लिए)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            black_screen, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2), # ग्रीन जॉइंट्स
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2) # सफेद लाइनें
        )
        
        # डिस्प्ले पर अलर्ट
        cv2.putText(black_screen, "MOTION DETECTED", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 4. आउटपुट दिखाना (सिर्फ स्केलेटन, कोई असली वीडियो नहीं)
    cv2.imshow('OmniSense Privacy Monitor', black_screen)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()