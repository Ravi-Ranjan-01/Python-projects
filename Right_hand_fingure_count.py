import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
# Initialize detector with a detection confidence threshold
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    if not success:
        break

    # Find the hand and automatically draw landmarks/connections
    hands, img = detector.findHands(img)

    if hands:
        hand1 = hands[0]
        # cvzone has a built-in helper function that returns an array like [1, 1, 1, 0, 0]
        fingers = detector.fingersUp(hand1)
        total_fingers = fingers.count(1)
        
        cv2.putText(img, f'Fingers: {total_fingers}', (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("CVZone Finger Counter", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()