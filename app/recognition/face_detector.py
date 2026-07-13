import face_recognition


import face_recognition


def detect_faces(image):
    return face_recognition.face_locations(
        image,
        model="hog"
    )