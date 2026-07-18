from unicodedata import name

import streamlit as st
import cv2
import time

from datetime import datetime

from app.recognition.face_engine import FaceRecognitionEngine
from app.database.attendance import mark_attendance
from app.database.user import get_user_by_name



def get_display_status():

    hour = datetime.now().hour
    minute = datetime.now().minute

    current_minutes = hour * 60 + minute


    if 360 <= current_minutes < 480:
        # 06:00 - 08:00
        return "Present"


    elif 480 <= current_minutes < 720:
        # 08:00 - 12:00
        return "Late Present"


    else:
        # After 12:00
        return "Absent"




def live_attendance_page():


    st.title("📷 Live Attendance")

    if "unknown_count" not in st.session_state:

     st.session_state.unknown_count = 0

    st.write(
        "Real-time face recognition attendance system"
    )


    start = st.checkbox(
        "Start Camera"
    )


    frame_window = st.empty()

    status_window = st.empty()



    if start:


        engine = FaceRecognitionEngine()


        camera = cv2.VideoCapture(0)



        if not camera.isOpened():

            st.error(
                "Cannot open camera"
            )

            return



        status_window.success(
            "Camera started"
        )



        marked_users = set()



        while start:



            ret, frame = camera.read()



            if not ret:

                st.error(
                    "Camera frame error"
                )

                break




            locations, names = engine.recognize(
                frame
            )




            for (top, right, bottom, left), name in zip(
                locations,
                names
            ):



                color = (0, 0, 255)

                if name == "Unknown":

                  st.session_state.unknown_count += 1

                if name != "Unknown":


                    color = (0, 255, 0)



                    if name not in marked_users:



                        user = get_user_by_name(name)



                        if user:



                            result = mark_attendance(
                                user["id"],
                                100.0
                            )


                            print(
                                f"{name}: {result}"
                            )


                            status_window.success(
                                f"{name}: {result}"
                            )


                            marked_users.add(name)




                cv2.rectangle(
                    frame,
                    (left, top),
                    (right, bottom),
                    color,
                    2
                )



                current_time = datetime.now().strftime(
                    "%H:%M:%S"
                )


                attendance_status = get_display_status()



                display_text = (
                    f"{name} | "
                    f"{attendance_status} | "
                    f"{current_time}"
                )



                cv2.putText(
                    frame,
                    display_text,
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    color,
                    2
                )

            st.metric(
               "Unknown Faces",
                st.session_state.unknown_count
                )


            frame_window.image(
                frame,
                channels="BGR",
                width="stretch"
            )



            time.sleep(0.03)




        camera.release()



        status_window.info(
            "Camera stopped"
        )

        st.divider()

        st.caption(
        "AI Face Attendance System © 2026"
      )