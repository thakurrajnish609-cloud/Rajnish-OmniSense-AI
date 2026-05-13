if results.pose_landmarks:
        # लाइनों और बिंदुओं दोनों को हरा (Green) करने के लिए:
        mp_drawing.draw_landmarks(
            black_screen, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2), # बिंदुओं का रंग
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2) # लाइनों का रंग (सफ़ेद से हरा किया)
        )