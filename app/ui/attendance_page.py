import streamlit as st


from app.database.user import get_user_by_id


def attendance_page():

    st.title("📋 Attendance History")


    records = get_attendance_history()


    if not records:

        st.info("No attendance records found")

        return



    table_data = []


    for row in records:

        user = get_user_by_id(
            row["user_id"]
        )


        name = "Unknown"


        if user:
            name = user["name"]


        table_data.append(
            {
                "Name": name,
                "Date": row["date"],
                "Check In": row["check_in_time"],
                "Check Out": row["check_out_time"],
                "Status": row["status"],
                "Confidence": f"{row['confidence']}%"
            }
        )


    st.dataframe(
        table_data,
        use_container_width=True
    )
    
def get_attendance_history():

    """
    Get all attendance records
    """

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM attendance
        ORDER BY date DESC, time DESC
        """
    )


    records = cursor.fetchall()


    conn.close()


    return records
def get_attendance_history():

    """
    Get all attendance records
    """

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM attendance
        ORDER BY date DESC
        """
    )


    records = cursor.fetchall()


    conn.close()


    return records
def get_attendance_dataframe():

    import pandas as pd

    records = get_attendance_history()

    data = []

    for row in records:

        data.append(
            {
                "User ID": row["user_id"],
                "Date": row["date"],
                "Check In": row["check_in_time"],
                "Check Out": row["check_out_time"],
                "Status": row["status"]
            }
        )

    return pd.DataFrame(data)