import json
import cv2
import face_recognition
import numpy as np

from app.database.user import get_all_users


class FaceRecognitionEngine:

    def __init__(self):

        self.known_encodings = []
        self.known_names = []

        self.load_faces()


    def load_faces(self):

        users = get_all_users()


        for user in users:

            user_name = user["name"]

            encoding = json.loads(
                user["encoding"]
            )


            self.known_encodings.append(
                np.array(encoding)
            )


            self.known_names.append(
                user_name
            )


        print(
            f"Loaded {len(self.known_encodings)} face samples"
        )



    def recognize(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        locations = face_recognition.face_locations(
            rgb_frame
        )


        face_encodings = face_recognition.face_encodings(
            rgb_frame,
            locations
        )


        names = []


        for face_encoding in face_encodings:


            matches = face_recognition.compare_faces(
                self.known_encodings,
                face_encoding,
                tolerance=0.50
            )


            name = "Unknown"


            if True in matches:

                first_match = matches.index(True)

                name = self.known_names[first_match]


            names.append(name)


        return locations, names