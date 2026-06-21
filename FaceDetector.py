import cv2
import cvlib as cv

# 1. Webcam capture pipeline start karein
cap = cv2.VideoCapture(0)

print("Real-Time Gender Detection Active. Press 'q' to quit.")

while True:
    success, img = cap.read()
    if not success:
        break

    # 2. cvlib ka use karke face aur gender ek sath detect karein
    # cv.detect_face chehre ki location (bbox) nikalta hai
    faces, confidences = cv.detect_face(img)

    # Loop through all detected faces
    for face in faces:
        x1, y1, x2, y2 = face[0], face[1], face[2], face[3]

        # Pink Bounding Box draw karein face ke charo taraf
        cv2.rectangle(img, (x1, y1), (x2, y2), (180, 105, 255), 2)

        # Chehre ke area ko crop karke gender check karne ke liye bhejte hain
        face_crop = img[y1:y2, x1:x2]
        
        if face_crop.size > 0:
            try:
                # cv.detect_gender aapko direct gender aur confidence score dega
                labels, counts = cv.detect_gender(face_crop)
                
                if labels:
                    # Sabse zyada confidence wala gender select karein (Male/Female)
                    detected_gender = labels[0]
                    confidence_percent = int(counts[0] * 100)

                    # Green color me "Gender: Percentage" text box ke upar render karein
                    label = f'{detected_gender}: {confidence_percent}%'
                    cv2.putText(img, label, (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            except Exception as e:
                pass

    # Viewport stream window show karein
    cv2.imshow("Real-Time Gender Detector", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()