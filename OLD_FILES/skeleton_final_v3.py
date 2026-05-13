import cv2
import numpy as np

# कैमरा शुरू करें
cap = cv2.VideoCapture(0)

# पहला फ्रेम पढ़ने के लिए (Background subtraction के लिए)
ret, frame1 = cap.read()
ret, frame2 = cap.read()

print("--- OMNISENSE MOTION SENSING ACTIVE ---")
print("Privacy Status: 100% SECURE (No Human Face Shown)")

while cap.isOpened():
    # 1. दो फ्रेम्स के बीच का अंतर निकालें (Motion Detection)
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    
    # 2. हरकत वाली जगह पर 'Lines' या 'Contours' ढूंढें
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 3. काली स्क्रीन बनाना (Security के लिए)
    black_screen = np.zeros(frame1.shape, dtype=np.uint8)

    for contour in contours:
        if cv2.contourArea(contour) < 900: # छोटी हरकतों को नज़रअंदाज़ करें
            continue
        
        # सिर्फ इंसान की बाहरी लाइनें (Skeleton जैसा लुक) ड्रा करें
        cv2.drawContours(black_screen, [contour], -1, (255, 255, 255), 2)
        
        # स्टेटस अपडेट
        cv2.putText(black_screen, "MOTION DETECTED", (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # आउटपुट दिखाएं
    cv2.imshow('CSI Style Sensing Monitor', black_screen)

    # अगले फ्रेम की तैयारी
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()