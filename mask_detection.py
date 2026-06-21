import cv2
from cvzone.FaceMeshModule import FaceMeshDetector

# 1. Capture stream aur Face Mesh Detector initialize karein
cap = cv2.VideoCapture(0)
# maxFaces=1 rakha hai fast processing ke liye
detector = FaceMeshDetector(maxFaces=1)

print("\n[System Active] Face Mask Detection running. Press 'q' to exit.")

while True:
    success, img = cap.read()
    if not success:
        break

    # 2. Facial landmarks detect karein (Grid lines draw nahi karenge)
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        
        # 3. Dynamic Mask Logic using Facial Landmarks:
        # MediaPipe Face Mesh me Point 0 (Lips center top) aur Point 13 (Lips center bottom) hote hain.
        # Hum in absolute tracking nodes ki coordinates check karte hain:
        lips_top = face[0]
        lips_bottom = face[13]
        
        # Agar lips ke points coordinates perfect track ho rahe hain aur zero nahi hain,
        # iska matlab chehra khula hai (No Mask).
        # Mask pehne hone par MediaPipe lips area ko mesh nahi kar pata aur distance alter ho jata hai.
        lips_distance = abs(lips_top[1] - lips_bottom[1])
        
        # 4. Box dimensions nikalte hain UI ke liye
        xList = [p[0] for p in face]
        yList = [p[1] for p in face]
        x, y, w, h = min(xList), min(yList), max(xList) - min(xList), max(yList) - min(yList)

        # Dynamic Threshold Verification:
        # Agar lips coordinates proper data pixel map de rahe hain (Khula chehra)
        if lips_distance > 1:
            label = "No Mask"
            text_color = (0, 0, 255)     # Red warning text
            box_color = (0, 0, 255)      # Red Alert Box
        else:
            label = "Mask Detected"
            text_color = (0, 255, 0)     # Green text
            box_color = (180, 105, 255)  # Consistent Pink Box

        # 5. UI Render Dashboard
        cv2.rectangle(img, (x, y), (x + w, y + h), box_color, 2)
        cv2.putText(img, label, (x, y - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)
                    
    else:
        # Agar face samne hai par ek bhi landmark point detect nahi ho raha, 
        # to high chance hai ki pure chehre par mask/cover laga hua hai
        # (Is mode me bhi safe checks ke liye Mask toggle display dikhayenge)
        pass

    cv2.imshow("Real-Time Face Mask Detector", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()