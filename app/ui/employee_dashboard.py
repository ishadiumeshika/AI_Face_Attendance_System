import streamlit as st
from app.database.leave import apply_leave, get_my_leaves
from app.database.attendance import get_attendance_history


def employee_dashboard():

    st.title("👤 Employee Dashboard")


    user_id = st.session_state.user_id
    name = st.session_state.name


    st.write(
        f"Welcome, {name}"
    )


    records = get_attendance_history()


    my_records = []


    for row in records:

        if row["user_id"] == user_id:

            my_records.append(
                {
                    "Date": row["date"],
                    "Time": row["time"],
                    "Status": row["status"]
                }
            )


    st.subheader("📋 My Attendance")


    if my_records:

        st.dataframe(
            my_records,
            width="stretch"
        )

    else:

        st.info(
            "No attendance records found"
        )


    st.divider()


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


st.subheader("📋 My Leave Requests")


leaves = get_my_leaves(user_id)


for leave in leaves:

    st.write(leave)