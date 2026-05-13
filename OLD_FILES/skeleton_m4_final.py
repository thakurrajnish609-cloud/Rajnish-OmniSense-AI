import cv2
import mediapipe as mp
import numpy as np
import time

# 1. New Tasks API का इस्तेमाल (Bypassing 'solutions')
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# पोज़ डिटेक्शन मॉडल का पाथ (इसे डाउनलोड करना होगा)
model_path = 'pose_landmarker_heavy.task'

# डिटेक्शन के बाद ड्रा करने का फंक्शन (Manual Drawing)
def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.zeros(rgb_image.shape, dtype=np.uint8) # काली स्क्रीन (Privacy)

    for idx in range(len(pose_landmarks_list)):
        landmarks = pose_landmarks_list[idx]
        for lm in landmarks:
            h, w, _ = rgb_image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(annotated_image, (cx, cy), 3, (0, 255, 0), -1) # ग्रीन जॉइंट्स
    return annotated_image

# 2. कॉन्फ़िगरेशन
options = vision.PoseLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    running_mode=vision.RunningMode.VIDEO)

cap = cv2.VideoCapture(0)

with vision.PoseLandmarker.create_from_options(options) as landmarker:
    print("--- OMNISENSE M4 SENSING: ACTIVE ---")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        timestamp = int(time.time() * 1000)
        
        # डिटेक्शन रन करें
        detection_result = landmarker.detect_for_video(mp_image, timestamp)
        
        # ड्रा करें (सिर्फ स्केलेटन)
        skeleton_frame = draw_landmarks_on_image(frame, detection_result)

        cv2.imshow('Skeleton Monitor (M4 Optimized)', skeleton_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()