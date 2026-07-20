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
        return "Present"


    elif 480 <= current_minutes < 720:
        return "Late Present"


    else:
        return "Absent"





def live_attendance_page():


    st.title("📷 Live Attendance")


    st.write(
        "Real-time face recognition attendance system"
    )


    # Session counter

    if "unknown_count" not in st.session_state:

        st.session_state.unknown_count = 0



    st.markdown("""
    <style>
    div.stButton > button {
       width: 300px;
       height: 90px;
       font-size: 28px;
       border-radius: 20px;
       margin: auto;
       display: block;
    }
    </style>
    """, unsafe_allow_html=True)

    start = st.button("📷 Open Camera")



    # Streamlit placeholders

    frame_window = st.empty()

    status_window = st.empty()

    unknown_window = st.empty()



    if start:


        engine = FaceRecognitionEngine()


        camera = cv2.VideoCapture(0)



        if not camera.isOpened():

            st.error(
                "❌ Cannot open camera"
            )

            return



        status_window.success(
            "📷 Camera started"
        )


        marked_users = set()



        while start:


            ret, frame = camera.read()



            if not ret:

                status_window.error(
                    "Camera frame error"
                )

                break




            locations, names = engine.recognize(
                frame
            )



            for (top, right, bottom, left), person_name in zip(
                locations,
                names
            ):



                color = (0,0,255)



                if person_name == "Unknown":


                    st.session_state.unknown_count += 1



                else:


                    color = (0,255,0)



                    if person_name not in marked_users:


                        user = get_user_by_name(
                            person_name
                        )



                        if user:


                            result = mark_attendance(
                                user["id"],
                                100.0
                            )


                            status_window.success(
                                f"✅ {person_name}: {result}"
                            )


                            marked_users.add(
                                person_name
                            )




                # Draw face box

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



                text = (
                    f"{person_name} | "
                    f"{attendance_status} | "
                    f"{current_time}"
                )



                cv2.putText(
                    frame,
                    text,
                    (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )



            # Update only one metric

            unknown_window.metric(
                "Unknown Faces",
                st.session_state.unknown_count
            )



            # Display camera

            frame_window.image(
                frame,
                channels="BGR",
                width="stretch"
            )



            time.sleep(0.03)




        camera.release()



        status_window.info(
            "⏹ Camera stopped"
        )



    st.divider()


    st.caption(
        "AI Face Attendance System © 2026"
    )