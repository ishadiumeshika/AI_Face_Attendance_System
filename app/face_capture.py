import cv2
import face_recognition
import time



def capture_faces(sample_count=20):


    camera = cv2.VideoCapture(0)


    if not camera.isOpened():

        return None



    encodings = []



    while len(encodings) < sample_count:


        ret, frame = camera.read()


        if not ret:

            break



        cv2.imshow(
            "Face Verification - Press Q",
            frame
        )



        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        faces = face_recognition.face_encodings(
            rgb
        )



        if len(faces) > 0:


            encodings.append(
                faces[0].tolist()
            )


            time.sleep(0.3)



        if cv2.waitKey(1) == ord("q"):

            break



    camera.release()

    cv2.destroyAllWindows()



    if len(encodings) == sample_count:

        return encodings


    return None