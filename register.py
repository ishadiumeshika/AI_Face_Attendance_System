import cv2
import face_recognition
import time

from app.database.user import (
    add_user,
    add_face_encoding,
    get_user_by_name
)


def register_person(name):

    # Prevent duplicate names
    existing_user = get_user_by_name(name)

    if existing_user:
        print("User already registered!")
        return


    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Camera not found")
        return


    print("Look at the camera...")
    print("Starting capture...")


    encodings = []

    sample_count = 20


    while len(encodings) < sample_count:

        ret, frame = camera.read()

        if not ret:
            break


        cv2.imshow(
            "Face Registration - Press Q to quit",
            frame
        )


        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        faces = face_recognition.face_encodings(
            rgb_frame
        )


        if len(faces) > 0:

            encoding = faces[0]

            encodings.append(
                encoding.tolist()
            )


            print(
                f"Captured sample {len(encodings)}/{sample_count}"
            )


            time.sleep(0.3)



        key = cv2.waitKey(1)


        if key == ord("q"):
            break



    camera.release()
    cv2.destroyAllWindows()



    if len(encodings) < sample_count:

        print("Registration cancelled. Not enough samples.")
        return



    # Create user
    user_id = add_user(name)



    # Save all face samples
    for encoding in encodings:

        add_face_encoding(
            user_id,
            encoding
        )


    print(
        f"Registration completed for {name}"
    )

    print(
        f"Saved {len(encodings)} face samples"
    )



if __name__ == "__main__":

    name = input(
        "Enter person name: "
    )

    register_person(name)