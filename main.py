import streamlit as st

st.set_page_config(
    page_title="AI Face Attendance System",
    page_icon="👤",
    layout="wide"
)

st.title("👤 AI Face Attendance System")

st.write(
    """
    Welcome to the AI Face Attendance System.

    Features:
    - Register users
    - Capture face images
    - Recognize faces
    - Record attendance
    """
)

st.success("System is running successfully!")