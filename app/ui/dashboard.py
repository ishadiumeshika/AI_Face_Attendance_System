import streamlit as st
from datetime import datetime

from app.database.user import get_registered_users
from app.database.attendance import get_attendance_history


def show_dashboard():

    st.title("🤖 AI Face Attendance System")

    st.write(
        "An automated attendance management system "
        "using facial recognition technology."
    )

    st.divider()


    users = get_registered_users()
    attendance = get_attendance_history()


    # Dashboard metrics

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
    "👥 Registered Users",
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
            "📅 Today's Attendance",
            today_count
        )


    with col3:

        if attendance:

            latest = attendance[-1]

            st.metric(
                "🕒 Last Attendance",
                latest["time"]
            )

        else:

            st.metric(
                "🕒 Last Attendance",
                "No records"
            )


    st.divider()


    st.subheader("📋 Attendance Records")


    if attendance:


        data = []


        for row in attendance:

            data.append(
                {
                    "User ID": row["user_id"],
                    "Name": row["name"],
                    "Date": row["date"],
                    "Time": row["time"],
                    "Status": row["status"]
                }
            )


        st.dataframe(
            data,
            width="stretch"
        )


    else:

        st.info(
            "No attendance records yet"
        )


    st.divider()


    st.subheader("⚙️ System Information")


    st.success(
        "Face Recognition Engine: Active"
    )

    st.success(
        "Database Connection: Active"
    )
