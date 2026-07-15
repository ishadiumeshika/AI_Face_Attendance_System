import streamlit as st
import cv2
import face_recognition
import time

from app.database.user import (
    add_user,
    add_face_encoding,
    get_user_by_name
)


def register_page():

    st.title("📝 Register New User")


    st.write(
        "Create your account and register your face."
    )


    name = st.text_input(
        "Full Name"
    )


    email = st.text_input(
        "Email Address"
    )


    password = st.text_input(
        "Password",
        type="password"
    )



    if st.button("📷 Register Face"):


        if not name or not email or not password:

            st.error(
                "Please fill all fields."
            )

            return



    
        st.info(
            "Look at the camera. Capturing face samples..."
        )


        camera = cv2.VideoCapture(0)


        if not camera.isOpened():

            st.error(
                "Camera not found."
            )

            return



        encodings = []


        sample_count = 20


        camera_window = st.empty()



        while len(encodings) < sample_count:


            ret, frame = camera.read()


            if not ret:

                break



            camera_window.image(
                frame,
                channels="BGR"
            )



            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )



            faces = face_recognition.face_encodings(
                rgb_frame
            )



            if len(faces) > 0:


                encodings.append(
                    faces[0].tolist()
                )


                st.write(
                    f"Captured {len(encodings)}/{sample_count}"
                )


                time.sleep(0.3)



        camera.release()



        if len(encodings) < sample_count:


            st.error(
                "Face registration failed. Try again."
            )

            return



        # Create user account

        result = add_user(
            name,
            email,
            password
        )



        if result == "EMAIL_EXISTS":


            st.error(
                "❌ This email is already registered. Use another email."
            )

            return





        elif result == "ERROR":


            st.error(
                "❌ Registration failed."
            )

            return



        else:


            user_id = result



        # Save face encodings

        for encoding in encodings:


            add_face_encoding(
                user_id,
                encoding
            )



        st.success(
            f"✅ Registration completed. Your User ID is {user_id}"
        )


        st.info(
            f"Saved {len(encodings)} face samples."
        )