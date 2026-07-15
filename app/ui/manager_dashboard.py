import streamlit as st

from app.database.attendance import get_attendance_history
from app.database.user import get_registered_users


def manager_dashboard():

    st.title("👨‍💼 Manager Dashboard")


    st.write(
        "Welcome Manager"
    )


    st.subheader(
        "📋 All Employee Attendance"
    )


    records = get_attendance_history()


    data = []


    for row in records:

        data.append(
            {
                "User ID": row["user_id"],
                "Name": row["name"],
                "Date": row["date"],
                "Time": row["time"],
                "Status": row["status"]
            }
        )


    if data:

        st.dataframe(
            data,
            width="stretch"
        )

    else:

        st.info(
            "No attendance records"
        )


    st.divider()


    st.subheader(
        "👥 Registered Employees"
    )


    users = get_registered_users()


    user_data = []


    for user in users:

        user_data.append(
            {
                "ID": user["id"],
                "Name": user["name"]
            }
        )


    st.dataframe(
        user_data,
        width="stretch"
    )