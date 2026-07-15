from datetime import datetime

from app.database.db_connection import get_connection



def mark_attendance(user_id):


    conn = get_connection()

    cursor = conn.cursor()



    now = datetime.now()


    today = now.strftime("%Y-%m-%d")

    current_time = now.strftime("%H:%M:%S")



    # Check already marked today

    cursor.execute(
        """
        SELECT id

        FROM attendance

        WHERE user_id=?

        AND date=?

        """,
        (
            user_id,
            today
        )
    )


    exists = cursor.fetchone()



    if exists:

        conn.close()

        return False



    # Attendance status

    office_time = datetime.strptime(
        "08:00:00",
        "%H:%M:%S"
    ).time()



    if now.time() <= office_time:

        status = "Present"

    else:

        status = "Late Present"



    cursor.execute(
        """
        INSERT INTO attendance
        (
            user_id,
            date,
            time,
            status
        )

        VALUES (?, ?, ?, ?)

        """,
        (
            user_id,
            today,
            current_time,
            status
        )
    )



    conn.commit()

    conn.close()


    return status