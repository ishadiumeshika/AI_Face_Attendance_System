import streamlit as st
from datetime import datetime

from app.database.user import get_all_users
from app.database.attendance import get_attendance_history


def show_dashboard():

    st.title("👤 AI Face Attendance System")


    users = get_all_users()
    attendance = get_attendance_history()


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Registered Users",
            len(set([u["name"] for u in users]))
        )


    with col2:

        today = datetime.now().strftime("%Y-%m-%d")

        today_count = len(
            [
                x for x in attendance
                if x["date"] == today
            ]
        )


        st.metric(
            "Today's Attendance",
            today_count
        )


    st.divider()


    st.subheader("Attendance History")


    if attendance:

        data = []


        for row in attendance:

            data.append(
                {
                    "Name": row["name"],
                    "Date": row["date"],
                    "Time": row["time"]
                }
            )


        st.dataframe(
            data,
            use_container_width=True
        )


    else:

        st.info(
            "No attendance records yet"
        )



    st.divider()


    st.subheader("Actions")


    if st.button("📷 Start Camera Attendance"):

        st.info(
            "Run camera mode from terminal: python camera.py"
        )


    if st.button("👤 Register New Person"):

        st.info(
            "Run registration from terminal: python register.py"
        )