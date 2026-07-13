import streamlit as st
import cv2
import time
import face_recognition

from app.database.user import (
    add_user,
    add_face_encoding,
    get_user_by_name
)


def register_page():

    st.title("👤 Register New Person")


    name = st.text_input(
        "Enter person name"
    )


    if st.button("📷 Start Face Capture"):


        if name.strip() == "":

            st.warning(
                "Please enter a name"
            )

            return


        if get_user_by_name(name):

            st.error(
                "Person already registered"
            )

            return



        camera = cv2.VideoCapture(0)


        encodings = []


        progress = st.progress(0)


        window = st.empty()


        while len(encodings) < 20:


            ret, frame = camera.read()


            if not ret:
                break


            window.image(
                frame,
                channels="BGR"
            )


            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )


            faces = face_recognition.face_encodings(
                rgb
            )


            if faces:


                encodings.append(
                    faces[0].tolist()
                )


                progress.progress(
                    len(encodings)/20
                )


                time.sleep(0.3)



        camera.release()


        if len(encodings) == 20:


            user_id = add_user(name)


            for encoding in encodings:

                add_face_encoding(
                    user_id,
                    encoding
                )


            st.success(
                f"{name} registered successfully"
            )

        else:

            st.error(
                "Registration failed"
            )