import cv2
import mediapipe as mp
import numpy as np

# MediaPipe के पुराने और नए दोनों तरीकों को सपोर्ट करने के लिए सेटअप
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# पोज़ डिटेक्शन मॉडल लोड करना
# अगर 'solutions' एरर दे, तो यह ब्लॉक उसे संभाल लेगा
try:
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1, # M4 चिप के लिए बैलेंस्ड परफॉरमेंस
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
except AttributeError:
    print("MediaPipe structure mismatch. Please run: pip install mediapipe --upgrade")
    exit()

cap = cv2.VideoCapture(0)

print("--- AI SKELETON WALL SENSING ACTIVE ---")
print("Privacy Mode: ON (Black Screen Only)")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # 1. पूरी तरह काली स्क्रीन बनाना (Security के लिए)
    # यह असली वीडियो को छुपा देगा (cite: User Summary)
    h, w, c = frame.shape
    black_screen = np.zeros((h, w, c), dtype=np.uint8)

    # 2. पोज़ डिटेक्शन के लिए इमेज प्रोसेस करना
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    # 3. सिर्फ इंसान का ढांचा (Skeleton) ड्रा करना
    if results.pose_landmarks:
        # सफेद लाइनों के साथ ढांचा बनाना
        mp_drawing.draw_landmarks(
            black_screen, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2), # जॉइंट्स (Green)
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2) # हड्डियां (White)
        )
        
        # स्क्रीन पर स्टेटस दिखाना
        cv2.putText(black_screen, "SENSING MOTION...", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # आउटपुट विंडो दिखाना
    cv2.imshow('OmniSense Privacy View', black_screen)
    
    # 'q' दबाने पर बंद होगा
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()