import json
import numpy as np
import face_recognition

from app.database.user import get_all_users


def recognize_face(face_encoding):

    users = get_all_users()

    if len(users) == 0:
        return "Unknown"

    known_encodings = []
    names = []

    for user in users:
        encoding = json.loads(user["face_encoding"])

        known_encodings.append(
            np.array(encoding)
        )

        names.append(user["name"])


    matches = face_recognition.compare_faces(
        known_encodings,
        np.array(face_encoding)
    )


    face_distances = face_recognition.face_distance(
        known_encodings,
        np.array(face_encoding)
    )


    best_match = np.argmin(face_distances)


    if matches[best_match]:
        return names[best_match]

    return "Unknown"