import cv2

from app.recognition.face_detector import detect_faces
from app.recognition.face_encoder import encode_face_from_frame
from app.recognition.face_recognizer import recognize_face


def start_camera():

    video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("Camera not found")
        return


    while True:

        ret, frame = video.read()

        if not ret:
            break


        # Small image only for detection
        small_frame = cv2.resize(
            frame,
            (0, 0),
            fx=0.25,
            fy=0.25
        )

        rgb_small = small_frame[:, :, ::-1]


        # Detect faces
        small_locations = detect_faces(rgb_small)


        for small_location in small_locations:

            small_top, small_right, small_bottom, small_left = small_location


            # Convert coordinates to original frame
            top = small_top * 4
            right = small_right * 4
            bottom = small_bottom * 4
            left = small_left * 4


            # Add margin around face
            top = max(0, top - 20)
            left = max(0, left - 20)
            bottom = min(frame.shape[0], bottom + 20)
            right = min(frame.shape[1], right + 20)


            # Crop from ORIGINAL frame
            face_image = frame[
                top:bottom,
                left:right
            ]


            # Convert crop to RGB
            rgb_face = cv2.cvtColor(
                face_image,
                cv2.COLOR_BGR2RGB
            )


            name = "Unknown"


            if rgb_face.size != 0:

                encoding = encode_face_from_frame(rgb_face)


                if encoding is not None:
                    name = recognize_face(encoding)


            # Draw box
            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0,255,0),
                2
            )


            cv2.putText(
                frame,
                name,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )


        cv2.imshow(
            "AI Face Attendance Camera",
            frame
        )


        if cv2.waitKey(1) & 0xFF == ord("q"):
            break



    video.release()
    cv2.destroyAllWindows()