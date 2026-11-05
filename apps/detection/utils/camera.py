import cv2
import os

base_path = os.path.dirname(__file__)

face_path = os.path.join(base_path, "haarcascades", "haarcascade_frontalface_default.xml")
eye_path = os.path.join(base_path, "haarcascades", "haarcascade_eye.xml")

face_cascade = cv2.CascadeClassifier(face_path)
eye_cascade = cv2.CascadeClassifier(eye_path)


def start_camera(process_frame):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not working")
        return

    print("✅ Camera started...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Frame not captured")
            break

        # 🔄 FIX: Flip for correct orientation
        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 🔥 IMPROVED DETECTION
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=4,
            minSize=(50, 50)
        )

        if len(faces) == 0:
            cv2.putText(frame, "No Face Detected", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(20, 20)
            )

            # 🔥 CALL PIPELINE
            state = process_frame(frame, eyes)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        cv2.imshow("Driver Monitoring", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()