import face_recognition
import numpy as np


def encode_face(image_path):
    """
    Convert a face image file into a face encoding.
    Used during registration.
    """

    image = face_recognition.load_image_file(image_path)

    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        return None

    return encodings[0].tolist()



def encode_face_from_frame(frame):
    """
    Convert a camera frame into a face encoding.
    Used for live camera recognition.
    """

    encodings = face_recognition.face_encodings(frame)

    if len(encodings) == 0:
        return None

    return encodings[0].tolist()



def compare_faces(known_encoding, unknown_encoding, tolerance=0.6):
    """
    Compare two face encodings.
    """

    known = np.array(known_encoding)
    unknown = np.array(unknown_encoding)

    result = face_recognition.compare_faces(
        [known],
        unknown,
        tolerance=tolerance
    )

    return result[0]