import cv2
from cvzone.FaceMeshModule import FaceMeshDetector

# 1. Webcam capture pipeline hook start karein
cap = cv2.VideoCapture(0)

# 2. Face Mesh Detector initialize karein (Bina external files ke chalta hai)
detector = FaceMeshDetector(maxFaces=1)

print("Face Tracking & Feature Analysis Active. Press 'q' to quit.")

while True:
    success, img = cap.read()
    if not success:
        break

    # Facial landmarks aur grid lines detect karein
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        
        # Chehre ke vertical aur horizontal ratios coordinates se facial structure check karte hain
        # Landmark 10 (Forehead center) aur Landmark 152 (Chin center)
        eyebrow_left = face[70]
        eyebrow_right = face[300]
        chin = face[152]
        forehead = face[10]
        
        # Ek sample bounding box bounding dimensions text positions ke liye nikalte hain
        xList = [p[0] for p in face]
        yList = [p[1] for p in face]
        x, y, w, h = min(xList), min(yList), max(xList) - min(xList), max(yList) - min(yList)
        
        # Bounding box rectangle display draw karein (Pink Color)
        cv2.rectangle(img, (x, y), (x + w, y + h), (180, 105, 255), 2)
        
        # Nota: Industry me custom landmarks parameters extraction logic
        # Feature verification metrics display text formatting (Green Color)
        cv2.putText(img, "Tracking Features Active", (x, y - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Real-Time Face Metric Analyzer", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()