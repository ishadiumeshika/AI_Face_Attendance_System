import cv2
import face_recognition


from app.recognition.face_engine import FaceRecognitionEngine
from app.database.attendance import mark_attendance
from app.database.user import get_user_by_name


def main():

    engine = FaceRecognitionEngine()

    camera = cv2.VideoCapture(0)


    if not camera.isOpened():

        print("Camera not found")
        return


    print("Camera started...")
    print("Press Q to quit")


    while True:

        ret, frame = camera.read()


        if not ret:
            break



        locations, names = engine.recognize(frame)



        for (top, right, bottom, left), name in zip(
            locations,
            names
        ):


            color = (0,255,0)


            if name == "Unknown":

                color = (0,0,255)


            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                color,
                2
            )


            cv2.rectangle(
                frame,
                (left, bottom-35),
                (right, bottom),
                color,
                cv2.FILLED
            )


            cv2.putText(
                frame,
                name,
                (left+6, bottom-6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )



            if name != "Unknown":


                user = get_user_by_name(name)


                if user:


                    success = mark_attendance(
                        user["id"]
                    )


                    if success:

                        print(
                            f"Attendance marked: {name}"
                        )



        cv2.imshow(
            "AI Face Attendance System",
            frame
        )



        key = cv2.waitKey(1)


        if key == ord("q"):

            break



    camera.release()
    cv2.destroyAllWindows()


def start_camera():

    main()


if __name__ == "__main__":

    start_camera()