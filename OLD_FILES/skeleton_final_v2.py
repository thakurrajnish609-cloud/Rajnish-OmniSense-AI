import cv2
import mediapipe as mp
import numpy as np

# नए Tasks API का इस्तेमाल
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# मॉडल फाइल डाउनलोड करने की ज़रूरत हो सकती है, लेकिन हम पुराने ड्रॉइंग टूल्स का जुगाड़ करेंगे
mp_drawing = mp.solutions.drawing_utils if hasattr(mp.solutions, 'drawing_utils') else None

# अगर ऊपर वाला फेल हो जाए, तो यह 'Hard-Coded' बैकअप है
try:
    from mediapipe.python.solutions import pose as mp_pose
    from mediapipe.python.solutions import drawing_utils as mp_drawing
except:
    print("Trying alternative import...")

cap = cv2.VideoCapture(0)

# प्राइवेसी मोड एक्टिवेट
print("--- SKELETON MONITOR: STARTING ---")

with mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success: break

        # 1. काली स्क्रीन (Privacy Wall)
        black_screen = np.zeros(image.shape, dtype=np.uint8)

        # 2. पोज़ डिटेक्शन
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # 3. ड्रा करना
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                black_screen,
                results.pose_landmarks,
                mp.solutions.pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp.solutions.drawing_styles.get_default_pose_landmarks_style())

        cv2.imshow('WiFi CSI Style Monitor', black_screen)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()