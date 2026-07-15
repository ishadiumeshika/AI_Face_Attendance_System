from app.database.db_connection import get_connection



def apply_leave(
    user_id,
    reason,
    from_date,
    to_date
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO leave_requests
        (
            user_id,
            reason,
            from_date,
            to_date
        )

        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            reason,
            from_date,
            to_date
        )
    )


    conn.commit()

    conn.close()



def get_my_leaves(user_id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            reason,
            from_date,
            to_date,
            status

        FROM leave_requests

        WHERE user_id = ?

        ORDER BY id DESC
        """,
        (user_id,)
    )


    data = cursor.fetchall()


    conn.close()

    return data




def get_all_leaves():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT

            leave_requests.id,
            users.name,
            leave_requests.reason,
            leave_requests.from_date,
            leave_requests.to_date,
            leave_requests.status

        FROM leave_requests

        JOIN users

        ON leave_requests.user_id = users.id

        ORDER BY leave_requests.id DESC
        """
    )


    data = cursor.fetchall()


    conn.close()

    return data



def update_leave_status(
    leave_id,
    status
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE leave_requests

        SET status = ?

        WHERE id = ?

        """,
        (
            status,
            leave_id
        )
    )


    conn.commit()

    conn.close()