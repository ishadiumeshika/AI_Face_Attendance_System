from datetime import datetime
from app.database.db_connection import get_connection


def get_attendance_status():

    """
    Attendance Policy:

    06:00 - 08:00  -> Present
    08:00 - 11:59  -> Late Present
    After 11:59    -> Absent
    """

    current_time = datetime.now().time()

    present_end = datetime.strptime(
        "08:00",
        "%H:%M"
    ).time()

    late_end = datetime.strptime(
        "11:59",
        "%H:%M"
    ).time()

    if current_time <= present_end:

        return "Present"

    elif current_time <= late_end:

        return "Late Present"

    else:

        return "Absent"


def get_today_date():

    return datetime.now().strftime("%Y-%m-%d")


def get_current_time():

    return datetime.now().strftime("%H:%M:%S")


def check_existing_attendance(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM attendance
        WHERE user_id = ?
        AND date = ?
        """,
        (
            user_id,
            get_today_date()
        )
    )

    record = cursor.fetchone()

    conn.close()

    return record


def mark_attendance(user_id, confidence):

    """
    First Face:
        Check In

    Second Face:
        Check Out (10 AM - 5 PM)
    """

    conn = get_connection()
    cursor = conn.cursor()

    today = get_today_date()

    current_time = get_current_time()

    existing = check_existing_attendance(
        user_id
    )

    # ==================================
    # FIRST RECOGNITION -> CHECK IN
    # ==================================

    if existing is None:

        status = get_attendance_status()

        cursor.execute(
            """
            INSERT INTO attendance
            (
                user_id,
                date,
                time,
                check_in_time,
                status,
                confidence
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                today,
                current_time,
                current_time,
                status,
                confidence
            )
        )

        conn.commit()

        conn.close()

        return f"Checked In - {status}"

    # ==================================
    # SECOND RECOGNITION -> CHECK OUT
    # ==================================

    else:

        checkout_time = existing["check_out_time"]

        if checkout_time is None:

            checkout_start = datetime.strptime(
                "10:00",
                "%H:%M"
            ).time()

            checkout_end = datetime.strptime(
                "17:00",
                "%H:%M"
            ).time()

            current = datetime.now().time()

            if checkout_start <= current <= checkout_end:

                cursor.execute(
                    """
                    UPDATE attendance

                    SET check_out_time = ?

                    WHERE user_id = ?

                    AND date = ?
                    """,
                    (
                        current_time,
                        user_id,
                        today
                    )
                )

                conn.commit()

                conn.close()

                return "Checked Out"

            else:

                conn.close()

                return (
                    "Check-out allowed only "
                    "between 10:00 AM and 5:00 PM"
                )

        else:

            conn.close()

            return "Attendance already completed"


def get_attendance_history():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM attendance
        ORDER BY date DESC, check_in_time DESC
        """
    )

    records = cursor.fetchall()

    conn.close()

    return records
def get_attendance_percentage(user_id):

    records = get_attendance_history()

    total = len(records)

    mine = len(
        [
            r for r in records
            if r["user_id"] == user_id
            and r["status"] != "Absent"
        ]
    )

    if total == 0:

        return 0

    return round(
        (mine/total)*100,
        2
    )
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
                "Status": row["status"],
                "Confidence": row["confidence"]
            }
        )

    return pd.DataFrame(data)