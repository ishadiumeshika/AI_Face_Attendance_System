from datetime import datetime

from app.database.db_connection import get_connection


def mark_attendance(user_id):
    """
    Mark attendance for a user.
    Prevent duplicate entries on the same day.
    """

    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")


    # Check duplicate attendance
    cursor.execute(
        """
        SELECT id
        FROM attendance
        WHERE user_id = ? AND date = ?
        """,
        (user_id, today)
    )


    already_marked = cursor.fetchone()


    if already_marked:

        conn.close()

        return False



    # Insert attendance
    cursor.execute(
        """
        INSERT INTO attendance
        (user_id, date, time)

        VALUES (?, ?, ?)
        """,
        (
            user_id,
            today,
            current_time
        )
    )


    conn.commit()
    conn.close()


    return True



def get_attendance_history():

    """
    Return attendance history with names.
    """


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT

            attendance.id,
            users.name,
            attendance.date,
            attendance.time

        FROM attendance

        JOIN users

        ON attendance.user_id = users.id

        ORDER BY date DESC, time DESC
        """
    )


    history = cursor.fetchall()


    conn.close()


    return history