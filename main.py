import streamlit as st

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="AI Face Attendance System",
    page_icon="👤",
    layout="wide"
)

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("👤 AI Face Attendance")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👤 Register User",
        "📷 Take Attendance",
        "📋 Attendance History",
        "ℹ️ About"
    ]
)

# -------------------------------
# Dashboard
# -------------------------------
if page == "🏠 Dashboard":

    st.title("👤 AI Face Attendance System")

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Registered Users", "0")

    with col2:
        st.metric("Present Today", "0")

    with col3:
        st.metric("Absent", "0")

    with col4:
        st.metric("Attendance %", "0%")

    st.markdown("---")

    st.subheader("Welcome")

    st.write("""
    This system uses Artificial Intelligence to:

    ✅ Register new users

    ✅ Detect faces

    ✅ Recognize people

    ✅ Record attendance automatically
    """)

# -------------------------------
# Register User
# -------------------------------
elif page == "👤 Register User":

    st.title("👤 Register User")

    st.info("This page will be connected to the registration camera.")

# -------------------------------
# Attendance
# -------------------------------
elif page == "📷 Take Attendance":

    st.title("📷 Take Attendance")

    st.info("This page will start face recognition.")

# -------------------------------
# History
# -------------------------------
elif page == "📋 Attendance History":

    st.title("📋 Attendance History")

    st.info("Attendance records will appear here.")

# -------------------------------
# About
# -------------------------------
elif page == "ℹ️ About":

    st.title("ℹ️ About")

    st.write("""
    AI Face Attendance System

    Developed using:

    - Python
    - Streamlit
    - OpenCV
    - face_recognition
    - SQLite

    Developed by ishadi
    """)