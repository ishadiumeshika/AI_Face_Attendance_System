import streamlit as st
from streamlit_option_menu import option_menu

from app.ui.live_attendance import live_attendance_page
from app.ui.employee_dashboard import employee_dashboard
from app.ui.manager_dashboard import manager_dashboard

st.set_page_config(
    page_title="AI Face Attendance System",
    page_icon="👤",
    layout="wide"
)
st.markdown(
    """
    <style>

    section[data-testid="stSidebar"]{
        background-color:#111827;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Session State Initialization
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "name" not in st.session_state:
    st.session_state.name = None

if "role" not in st.session_state:
    st.session_state.role = None



# -----------------------------
# Sidebar Menu
# -----------------------------

with st.sidebar:

    st.title("👤 AI Attendance")


    menu = [
        "Live Attendance",
        "Login",
        "Register"
    ]


    # Add role-based menu items

    if st.session_state.logged_in:


        if st.session_state.role == "Employee":

            menu.append("My Attendance")


        elif st.session_state.role == "Manager":

            menu.append("Employee Attendance")


        menu.append("Logout")



    selected = option_menu(
        "Menu",
        menu,
        icons=[
            "camera",
            "box-arrow-in-right",
            "person-plus",
            "clipboard-data",
            "box-arrow-right"
        ],
        default_index=0
    )



    st.divider()



    # Current logged user

    if st.session_state.logged_in:

        st.success(
            f"👤 {st.session_state.name}"
        )

        st.info(
            f"Role: {st.session_state.role}"
        )



# -----------------------------
# Main Page Routing
# -----------------------------

if selected == "Live Attendance":

    live_attendance_page()



elif selected == "My Attendance":

    employee_dashboard()



elif selected == "Employee Attendance":

    manager_dashboard()



elif selected == "Login":

    from app.ui.login_page import login_page

    login_page()



elif selected == "Register":

    from app.ui.register_page import register_page

    register_page()



elif selected == "Logout":


    st.session_state.logged_in = False

    st.session_state.user_id = None

    st.session_state.name = None

    st.session_state.role = None


    st.success(
        "Logged out successfully"
    )


    st.rerun()
    st.divider()

    st.caption(
    "AI Face Attendance System © 2026"
    )