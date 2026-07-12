import face_recognition


def detect_faces(image):
    """
    Detect faces in an image.

    Returns:
        list of face locations
    """

    face_locations = face_recognition.face_locations(image)

    return face_locations