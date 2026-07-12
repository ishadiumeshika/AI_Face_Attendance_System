import face_recognition
import pickle
from pathlib import Path
import numpy as np

ENCODING_FILE = Path("encodings/face_encodings.pkl")


def save_encodings(data):
    ENCODING_FILE.parent.mkdir(exist_ok=True)

    with open(ENCODING_FILE, "wb") as file:
        pickle.dump(data, file)


def load_encodings():
    if not ENCODING_FILE.exists():
        return []

    with open(ENCODING_FILE, "rb") as file:
        return pickle.load(file)


def create_face_encoding(image_path):
    image = face_recognition.load_image_file(image_path)

    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        return None

    return encodings[0]


def compare_faces(known_encoding, unknown_encoding):
    result = face_recognition.compare_faces(
        [known_encoding],
        unknown_encoding,
        tolerance=0.5
    )

    return result[0]


def find_matching_face(unknown_encoding):
    known_faces = load_encodings()

    for person in known_faces:

        match = compare_faces(
            person["encoding"],
            unknown_encoding
        )

        if match:
            return person["student_id"], person["name"]

    return None, None