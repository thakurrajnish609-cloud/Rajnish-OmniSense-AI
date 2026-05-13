import cv2
import mediapipe as mp
import numpy as np
import time
import os

# --- 1. Mouse Logic for BACK Button ---
is_back_pressed = False
def mouse_callback(event, x, y, flags, param):
    global is_back_pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        # Back button area: x(10-110), y(10-50)
        if 10 <= x <= 110 and 10 <= y <= 50:
            is_back_pressed = True

# --- 2. Mediapipe Setup ---
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# --- 3. Variables ---
fall_start_time = None
is_fallen = False
pre_alert_done = False

# Camera Setup (Try 0 for MacBook camera)
cap = cv2.VideoCapture(0)

# Window Setup
window_name = 'Rajnish OmniSense - Smart AI Monitor'
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, mouse_callback)

print("System Started Successfully. Press 'BACK' or 'q' to exit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success or is_back_pressed:
        break

    h, w, c = frame.shape
    # Privacy Mode: Create Black Screen with Radar Grid
    screen = np.zeros((h, w, c), dtype=np.uint8)
    for i in range(0, h, 40): cv2.line(screen, (0, i), (w, i), (0, 30, 0), 1) # Wall Radar Grid
    for i in range(0, w, 40): cv2.line(screen, (i, 0), (i, h), (0, 30, 0), 1)

    # --- 4. UI: BACK Button ---
    cv2.rectangle(screen, (10, 10), (110, 50), (200, 200, 200), -1)
    cv2.putText(screen, "BACK", (35, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # --- 5. AI Skeleton Processing ---
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        # Fix for your error: using POSE_CONNECTIONS correctly
        mp_drawing.draw_landmarks(
            screen, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS, # This connects dots with lines
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=3, circle_radius=3), # Dots
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2)              # Lines
        )

        # --- 6. Smart Fall Logic ---
        landmarks = results.pose_landmarks.landmark
        nose_y = landmarks[mp_pose.PoseLandmark.NOSE].y
        ankle_y = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y
        body_height = abs(ankle_y - nose_y)

        # If body is horizontal (lying down)
        if body_height < 0.35:
            if not is_fallen:
                fall_start_time = time.time()
                is_fallen = True
                pre_alert_done = False
            
            elapsed = int(time.time() - fall_start_time)

            if elapsed <= 5:
                cv2.putText(screen, f"STILLNESS DETECTED: {elapsed}s", (150, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            elif elapsed <= 9:
                cv2.putText(screen, "ARE YOU OKAY?", (w//2-100, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 165, 255), 2)
                if not pre_alert_done:
                    os.system('say "Are you okay?" &') # Soft Voice
                    pre_alert_done = True
            else:
                # 10 Seconds Reached - FINAL ALARM
                cv2.rectangle(screen, (0, h//2-50), (w, h//2+50), (0, 0, 255), -1)
                cv2.putText(screen, "EMERGENCY: NO RESPONSE!", (w//2-220, h//2+10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
                os.system('say "Emergency! A person is down and not responding!" &')
                time.sleep(1) # Gap for voice
        else:
            # If person stands up (90 degrees), Reset Everything
            is_fallen = False
            fall_start_time = None
            pre_alert_done = False

    # --- 7. Final Output ---
    cv2.putText(screen, "WALL RADAR: SCANNING...", (w-250, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.imshow(window_name, screen)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == ord('b'):
        break

cap.release()
cv2.destroyAllWindows()

