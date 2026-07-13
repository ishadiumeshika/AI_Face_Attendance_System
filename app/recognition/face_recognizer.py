import json
import numpy as np
import face_recognition

from app.database.user import get_all_users


# Maximum accepted face distance
FACE_DISTANCE_THRESHOLD = 0.50


def recognize_face(face_encoding):
    """
    Recognize a face using all stored face encodings.
    Returns the user's name or 'Unknown'.
    """

    users = get_all_users()

    if not users:
        return "Unknown"

    known_encodings = []
    known_names = []

    # Load every stored face encoding
    for user in users:
        try:
            encoding = np.array(
                json.loads(user["encoding"]),
                dtype=np.float64
            )

            known_encodings.append(encoding)
            known_names.append(user["name"])

        except Exception:
            continue

    if len(known_encodings) == 0:
        return "Unknown"

    face_encoding = np.array(face_encoding, dtype=np.float64)

    # Calculate distances
    face_distances = face_recognition.face_distance(
        known_encodings,
        face_encoding
    )

    best_match_index = np.argmin(face_distances)
    best_distance = face_distances[best_match_index]

    print(
        f"Best Match: {known_names[best_match_index]} | Distance: {best_distance:.3f}"
    )

    if best_distance <= FACE_DISTANCE_THRESHOLD:
        return known_names[best_match_index]

    return "Unknown"