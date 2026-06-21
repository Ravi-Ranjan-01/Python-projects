import cv2
from cvzone.HandTrackingModule import HandDetector
import serial  # Remember the 'i'!
import time

# Initialize Serial Connection (Change 'COM3' to your actual Arduino port)
try:
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=0.1)
    time.sleep(2)  # Wait for Arduino to reset
    print("Arduino Connected!")
except Exception as e:
    print(f"Connection Error: {e}")
    arduino = None

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    if not success:
        break

    hands, img = detector.findHands(img)

    if hands:
        hand1 = hands[0]
        fingers = detector.fingersUp(hand1)  # Gives an array like [1, 1, 0, 0, 0]
        total_fingers = fingers.count(1)
        
        # --- NEW CODE TO TALK TO ARDUINO ---
        # Convert list [1, 1, 0, 0, 0] into a string "11000"
        finger_string = "".join(map(str, fingers))
        
        if arduino:
            arduino.write(bytes(finger_string, 'utf-8')) # Send it over USB!
        # ----------------------------------
        
        cv2.putText(img, f'Fingers: {total_fingers}', (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    else:
        # If no hand is on screen, tell Arduino to turn everything off
        if arduino:
            arduino.write(bytes("00000", 'utf-8'))

    cv2.imshow("CVZone Finger Counter", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if arduino:
    arduino.close()
cap.release()
cv2.destroyAllWindows()