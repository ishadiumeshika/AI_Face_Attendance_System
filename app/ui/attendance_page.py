import streamlit as st
import cv2

from datetime import datetime

from app.recognition.face_engine import FaceRecognitionEngine
from app.database.attendance import mark_attendance
from app.database.user import get_user_by_name



def live_attendance_page():

    st.title("📷 Live Attendance")


    # Camera button

    if "camera_started" not in st.session_state:
        st.session_state.camera_started = False



    if not st.session_state.camera_started:


        st.markdown(
            """
            <style>
            div.stButton > button {
                width: 250px;
                height: 150px;
                font-size: 60px;
                border-radius: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


        col1, col2, col3 = st.columns(3)


        with col2:

            if st.button("📷"):

                st.session_state.camera_started = True

                st.rerun()



        st.info(
            "Click the camera button to start attendance"
        )


        return



    # Camera started

    st.success(
        "Camera started. Face the camera."
    )


    engine = FaceRecognitionEngine()


    camera = cv2.VideoCapture(0)


    frame_window = st.empty()


    stop_button = st.button(
        "⛔ Stop Camera"
    )



    while not stop_button:


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


            color = (0,0,255)

            display_text = name



            if name != "Unknown":


                color = (0,255,0)


                user = get_user_by_name(
                    name
                )


                if user:


                    marked = mark_attendance(
                        user["id"]
                    )


                    current_time = datetime.now().strftime(
                        "%H:%M:%S"
                    )


                    display_text = (
                        f"{name} | {current_time}"
                    )


                    if marked:

                        st.success(
                            f"Attendance marked: {name}"
                        )



            cv2.rectangle(
                frame,
                (left,top),
                (right,bottom),
                color,
                2
            )


            cv2.putText(
                frame,
                display_text,
                (left, top-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )



        frame_window.image(
            frame,
            channels="BGR",
            width="stretch"
        )



    camera.release()

    cv2.destroyAllWindows()


    st.session_state.camera_started = False

    st.rerun()