import cv2
import face_recognition

from app.database.user import add_user


def register_person(name):

    camera = cv2.VideoCapture(0)

    print("Look at the camera...")

    while True:

        ret, frame = camera.read()

        if not ret:
            break


        cv2.imshow(
            "Register Face - Press S to Save",
            frame
        )


        key = cv2.waitKey(1)


        if key == ord("s"):

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )


            encodings = face_recognition.face_encodings(
                rgb_frame
            )


            if len(encodings) == 0:
                print("No face detected")
                continue


            encoding = encodings[0].tolist()


            user_id = add_user(
                name,
                encoding
            )


            print(
                f"Registered successfully. User ID: {user_id}"
            )

            break


        elif key == ord("q"):
            break


    camera.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":

    name = input("Enter person name: ")

    register_person(name)