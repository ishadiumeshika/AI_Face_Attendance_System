import streamlit as st
import sqlite3
import pandas as pd


st.title("📋 Attendance History")

DB_PATH = "database/attendance.db"


def get_attendance_history():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT 
        users.name AS Name,
        attendance.date AS Date,
        attendance.time AS Time,
        attendance.status AS Status
    FROM attendance
    JOIN users
    ON attendance.user_id = users.id
    ORDER BY attendance.date DESC, attendance.time DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


attendance = get_attendance_history()


if attendance.empty:

    st.warning("No attendance records found.")

else:

    st.dataframe(
        attendance,
        width="stretch"
    )