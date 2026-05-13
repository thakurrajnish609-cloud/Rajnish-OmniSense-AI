import cv2

# कैमरा शुरू करना
cap = cv2.VideoCapture(0)

print("Elderly Safety Monitor is LIVE. Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # इमेज को ग्रे (Grayscale) करना ताकि प्रोसेस आसान हो
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # सिर्फ हलचल (Movement) वाले हिस्से को पहचानना
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000: continue # छोटी हलचल को इग्नोर करें
        
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # अगर शरीर की ऊंचाई (y) स्क्रीन के नीचे वाले हिस्से (70%) में चली जाए
        if y > (frame.shape[0] * 0.7):
            cv2.putText(frame, "⚠️ FALL DETECTED!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
            print("ALERT: Possible Fall!")

    cv2.imshow('Rajnish Elder Guard - Live Monitor', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()