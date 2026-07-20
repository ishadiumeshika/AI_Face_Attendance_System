import email

import streamlit as st
import cv2
import face_recognition
import time

from app.database.user import (
    add_user,
    add_face_encoding
)
import re


def is_valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email)


def is_valid_password(password):
    return (
        len(password) >= 8
        and any(char.isupper() for char in password)
        and any(char.islower() for char in password)
        and any(char.isdigit() for char in password)
    )

def register_page():

    st.title("📝 Register New User")

    st.write(
        "Create your account and register your face."
    )


    # User details
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
    st.info(
    """
    Password Requirements:
    - Minimum 8 characters
    - One uppercase letter
    - One lowercase letter
    - One number
    """
    )

    st.divider()


    if st.button("📷 Register Face"):


        # Validation

        # Validation

        if not name or not email or not password:

            st.error(
                 "⚠️ Please fill all fields."
            )

            return


        if not is_valid_email(email):

            st.error(
            "❌ Invalid email address.\n"
            "Example: user@gmail.com"
            )

            return


        if not is_valid_password(password):

            st.error(
                """
                ❌ Password must contain:

                • At least 8 characters
                • One uppercase letter
                • One lowercase letter
                • One number
                """
          )

            return



        st.info(
            "Look at the camera. Capturing face samples..."
        )


        # Open camera

        camera = cv2.VideoCapture(0)


        if not camera.isOpened():

            st.error(
                "❌ Camera not found."
            )

            return



        encodings = []

        sample_count = 20


        # UI containers

        camera_window = st.empty()

        progress_text = st.empty()

        progress_bar = st.progress(0)



        # Capture faces

        while len(encodings) < sample_count:


            ret, frame = camera.read()


            if not ret:

                st.error(
                    "Camera error."
                )

                break



            # Show camera

            camera_window.image(
                frame,
                channels="BGR"
            )



            # Convert frame

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )



            # Detect face encoding

            faces = face_recognition.face_encodings(
                rgb_frame
            )



            if len(faces) > 0:


                encodings.append(
                    faces[0].tolist()
                )


                current = len(encodings)


                progress_text.write(
                    f"Captured {current}/{sample_count} face samples"
                )


                progress_bar.progress(
                    current / sample_count
                )


                time.sleep(0.3)



        camera.release()


        camera_window.empty()



        # Check capture result

        if len(encodings) < sample_count:


            st.error(
                "❌ Face registration failed. Please try again."
            )

            return



        st.success(
            "✅ Face samples captured successfully."
        )



        # Create user account

        result = add_user(
            name,
            email,
            password
        )



        if result == "EMAIL_EXISTS":


            st.error(
                "❌ This email is already registered."
            )

            return



        elif isinstance(result, str):


            st.error(
               f"❌ Registration failed: {result}"
      )

            
            
            st.write(
                 "Check terminal for database error."
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



        # Final message

        st.success(
            "🎉 Registration completed successfully!"
        )


        st.info(
            f"""
            User ID: {user_id}

            Saved Face Samples: {len(encodings)}
            """
        )