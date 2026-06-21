import cv2
from cvzone.FaceDetectionModule import FaceDetector

cap = cv2.VideoCapture(0)
detector = FaceDetector(minDetectionCon=0.5)

while True:
    success, img = cap.read()
    if not success:
        break

    # Face detect karein aur boxes draw karein
    img, bboxs = detector.findFaces(img, draw=True)

    if bboxs:
        face1 = bboxs[0]
        detection_score = face1["score"][0]
        confidence_percentage = int(detection_score * 100)
        
        # Bounding box ke exact coordinates nikalte hain [x, y, width, height]
        x, y, w, h = face1["bbox"]
        
        # FIXED: Text ko face box ke thoda upar (y - 20) draw karenge 
        # Isse coordinates kabhi cutenge nahi aur text hamesha chehre ke sath chalega
        cv2.putText(img, f'{confidence_percentage}%', (x, y - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("CVZone Face Detector", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()