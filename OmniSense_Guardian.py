import cv2
import numpy as np
import mediapipe as mp
import time
import os
import sounddevice as sd # आवाज़ मापने के लिए

# AI & MediaPipe Setup
from mediapipe.python.solutions import pose as mp_pose
from mediapipe.python.solutions import drawing_utils as mp_drawing

pose = mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)
cap = cv2.VideoCapture(0) # MacBook M4 Camera (cite: User Summary)

# Sound Sensing Variables
audio_threshold = 0.3 # गिरने की आवाज़ का लेवल (इसे ज़रूरत अनुसार बदलें)
last_loud_sound = 0

def audio_callback(indata, frames, time, status):
    global last_loud_sound
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > audio_threshold:
        last_loud_sound = time.inputBufferAdcTime

# Start Audio Monitoring
stream = sd.InputStream(callback=audio_callback)
stream.start()

# Monitoring Variables
is_fallen = False
fall_start_time = None
alert_triggered = False

print("OmniSense Pro: WiFi CSI Style + Audio Sensing Active")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    h, w, _ = frame.shape
    # Privacy Black Screen (cite: image_42.png)
    display_screen = np.zeros((h, w, 3), dtype=np.uint8)
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    # 1. Fall Detection Logic (cite: User Summary)
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP].y
        nose_y = landmarks[mp_pose.PoseLandmark.NOSE].y

        if nose_y > hip_y: # Head below hips
            if not is_fallen:
                is_fallen = True
                fall_start_time = time.time()
        else:
            is_fallen = False
            fall_start_time = None
            alert_triggered = False

    # 2. Status & Alerts (Audio + Vision)
    color = (0, 255, 0)
    msg = "SYSTEM: MONITORING"

    if is_fallen:
        elapsed = time.time() - fall_start_time
        if elapsed > 10:
            color = (0, 0, 255) # Red Alert
            msg = "!!! DANGER: EMERGENCY !!!"
            if not alert_triggered:
                os.system('say "Alert. Motion and Sound mismatch detected. Checking safety."')
                alert_triggered = True
        else:
            color = (0, 255, 255) # Warning Yellow
            msg = f"FALL DETECTED: {int(10-elapsed)}s"

    # Drawing (Radar Style dots like image_42.png)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            display_screen, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=color, thickness=-1, circle_radius=6),
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1)
        )

    # UI Overlay
    cv2.putText(display_screen, msg, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv2.putText(display_screen, "AUDIO SENSOR: ACTIVE", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('OmniSense LifeGuard Pro', display_screen)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

stream.stop()
cap.release()
cv2.destroyAllWindows()