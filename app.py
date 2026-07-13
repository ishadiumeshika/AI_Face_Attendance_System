import streamlit as st

from streamlit_option_menu import option_menu

from app.ui.dashboard import show_dashboard


st.set_page_config(
    page_title="AI Face Attendance System",
    page_icon="👤",
    layout="wide"
)


with st.sidebar:

    selected = option_menu(
        "AI Attendance",
        [
            "Dashboard",
            "Register Person",
            "Live Attendance",
            "Attendance History",
            "Manage Users"
        ],
        icons=[
            "house",
            "person-plus",
            "camera",
            "clipboard-data",
            "people"
        ]
    )


if selected == "Dashboard":

    show_dashboard()


elif selected == "Register Person":

    from app.ui.register_page import register_page

    register_page()


elif selected == "Live Attendance":

    from app.ui.live_attendance import live_attendance_page

    live_attendance_page()


elif selected == "Attendance History":

    from app.ui.attendance_page import attendance_page

    attendance_page()