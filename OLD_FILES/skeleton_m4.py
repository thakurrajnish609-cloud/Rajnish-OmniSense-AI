import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

# सही पाथ जो आपकी MacBook Air M4 के लिए है (cite: User Summary)
model_path = '/Users/rajnish/My_AI_Project/pose_landmarker.task'

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    output_segmentation_masks=True
)

print("M4 Privacy Mode: ON. Press 'q' to quit.")

with vision.PoseLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        # AI Processing यहाँ होगी...
        cv2.imshow('Skeleton View', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()