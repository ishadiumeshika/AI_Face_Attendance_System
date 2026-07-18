import streamlit as st

from app.database.leave import apply_leave, get_my_leaves
from app.database.attendance import get_attendance_history
from app.database.attendance import (
    get_attendance_percentage
)


def employee_dashboard():

    st.title("👤 Employee Dashboard")


    user_id = st.session_state.user_id
    name = st.session_state.name

    percentage = get_attendance_percentage(
    user_id
    )

    st.metric(
    "Attendance %",
    f"{percentage}%"
    ) 
    st.write(
        f"Welcome, {name}"
    )


    # -----------------------------
    # Attendance History
    # -----------------------------

    records = get_attendance_history()


    my_records = []


    for row in records:


        if row["user_id"] == user_id:


            my_records.append(
                {
                    "Date": row["date"],

                    "Check In": row["check_in_time"],

                    "Check Out": row["check_out_time"]
                    if row["check_out_time"]
                    else "-",

                    "Status": row["status"],

                    "Confidence": 
                    f"{row['confidence']}%"
                    if row["confidence"]
                    else "-"
                }
            )



    st.subheader("📋 My Attendance")



    if my_records:


        st.dataframe(
            my_records,
            use_container_width=True
        )


    else:

        st.info(
            "No attendance records found"
        )



    st.divider()



    # -----------------------------
    # Apply Leave
    # -----------------------------

    st.subheader("🏖 Apply Leave")


    reason = st.text_area(
        "Reason"
    )


    from_date = st.date_input(
        "From Date"
    )


    to_date = st.date_input(
        "To Date"
    )



    if st.button("Submit Leave"):


        apply_leave(

            user_id,

            reason,

            str(from_date),

            str(to_date)

        )


        st.success(
            "Leave request submitted"
        )



    st.divider()



    # -----------------------------
    # Leave History
    # -----------------------------

    st.subheader("📋 My Leave Requests")


    leaves = get_my_leaves(user_id)



    if leaves:

        for leave in leaves:

            st.write(leave)


    else:

        st.info(
            "No leave requests found"
        )
        st.divider()

    st.caption(
    "AI Face Attendance System © 2026"
    )