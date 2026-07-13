import cv2
import face_recognition


def encode_face_from_frame(frame):
    """
    Convert a face image from camera frame into a face encoding.

    Input:
        frame - OpenCV image (BGR)

    Output:
        128-d face encoding or None
    """

    try:

        # Check image exists
        if frame is None:
            return None


        # Check image is not empty
        if frame.size == 0:
            return None


        # Convert OpenCV BGR image to RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        # Generate face encodings
        encodings = face_recognition.face_encodings(
            rgb_frame
        )


        # No face found
        if len(encodings) == 0:
            return None


        # Return first face encoding
        return encodings[0]


    except Exception as e:

        print("Face encoding error:", e)

        return None