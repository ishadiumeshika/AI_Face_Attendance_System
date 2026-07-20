import streamlit as st

from app.database.attendance import (
    get_attendance_history,
    get_attendance_dataframe
)

from app.database.user import (
    get_all_users,
    get_user_by_id,
    get_total_employees
)

from app.database.leave import (
    get_all_leaves,
    update_leave_status
)


def manager_dashboard():

    st.title("👨‍💼 Manager Dashboard")

    st.write(
        "Welcome Manager"
    )

    # =====================================
    # LOAD DATA
    # =====================================

    records = get_attendance_history()

    users = get_all_users()

    leaves = get_all_leaves()

    # =====================================
    # DASHBOARD STATISTICS
    # =====================================

    total_employees = get_total_employees()

    present = len(
        [r for r in records if r["status"] == "Present"]
    )

    late = len(
        [r for r in records if r["status"] == "Late Present"]
    )

    pending = len(
        [l for l in leaves if l["status"] == "Pending"]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Employees",
            total_employees
        )

    with col2:
        st.metric(
            "Present",
            present
        )

    with col3:
        st.metric(
            "Late",
            late
        )

    with col4:
        st.metric(
            "Pending Leaves",
            pending
        )

    st.divider()

    # =====================================
    # ATTENDANCE RECORDS
    # =====================================

    st.subheader(
        "📋 All Employee Attendance"
    )

    data = []

    for row in records:

        user = get_user_by_id(
            row["user_id"]
        )

        name = "Unknown"

        if user:
            name = user["name"]

        data.append(
            {
                "Name": name,
                "Date": row["date"],
                "Check In": row["check_in_time"],
                "Check Out":
                    row["check_out_time"]
                    if row["check_out_time"]
                    else "-",
                "Status": row["status"],
                
            }
        )

    if data:

        st.dataframe(
            data,
            use_container_width=True
        )

    else:

        st.info(
            "No attendance records"
        )

    st.divider()

    # =====================================
    # REGISTERED EMPLOYEES
    # =====================================

    st.subheader(
        "👥 Registered Employees"
    )

    user_data = []

    for user in users:

        user_data.append(
            {
                "Employee ID": user["employee_id"],
                "Name": user["name"],
                "Role": user["role"]
            }
        )

    if user_data:

        st.dataframe(
            user_data,
            use_container_width=True
        )

    else:

        st.info(
            "No registered employees"
        )

    st.divider()

    # =====================================
    # LEAVE REQUESTS
    # =====================================

    st.subheader(
        "🏖 Employee Leave Requests"
    )

    if leaves:

        for leave in leaves:

            st.write(
                f"### {leave['name']}"
            )

            st.write(
                f"Reason: {leave['reason']}"
            )

            st.write(
                f"From: {leave['from_date']}"
            )

            st.write(
                f"To: {leave['to_date']}"
            )

            st.write(
                f"Status: {leave['status']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    f"Approve {leave['id']}"
                ):

                    update_leave_status(
                        leave["id"],
                        "Approved"
                    )

                    st.rerun()

            with col2:

                if st.button(
                    f"Reject {leave['id']}"
                ):

                    update_leave_status(
                        leave["id"],
                        "Rejected"
                    )

                    st.rerun()

            st.divider()

    else:

        st.info(
            "No leave requests found"
        )

    # =====================================
    # CSV DOWNLOAD
    # =====================================

    df = get_attendance_dataframe()

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        "Download Attendance CSV",
        csv,
        "attendance.csv",
        "text/csv"
    )

    # =====================================
    # FOOTER
    # =====================================

    st.divider()

    st.caption(
        "AI Face Attendance System © 2026"
    )