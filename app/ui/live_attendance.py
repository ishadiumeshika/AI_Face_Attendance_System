import streamlit as st
import cv2

from app.recognition.face_engine import FaceRecognitionEngine
from app.database.attendance import mark_attendance
from app.database.user import get_user_by_name



def live_attendance_page():

    st.title("📷 Live Attendance")


    start = st.checkbox(
        "Start Camera"
    )


    frame_window = st.empty()


    if start:


        engine = FaceRecognitionEngine()


        camera = cv2.VideoCapture(0)



        while True:


            ret, frame = camera.read()


            if not ret:

                break



            locations, names = engine.recognize(
                frame
            )



            for (top, right, bottom, left), name in zip(
                    locations,
                    names
            ):



                color = (0, 0, 255)



                if name != "Unknown":


                    color = (0, 255, 0)



                    user = get_user_by_name(
                        name
                    )



                    if user:


                        status = mark_attendance(
                            user["id"]
                        )



                        if status:


                            st.success(
                                f"{name} - {status}"
                            )



                cv2.rectangle(
                    frame,
                    (left, top),
                    (right, bottom),
                    color,
                    2
                )



                cv2.putText(
                    frame,
                    name,
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    color,
                    2
                )



            frame_window.image(
                frame,
                channels="BGR"
            )



        camera.release()