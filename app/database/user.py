import json
from app.database.db_connection import get_connection


def add_user(name, face_encoding):
    """
    Add a new user with face encoding.
    """

    conn = get_connection()
    cursor = conn.cursor()

    encoding_json = json.dumps(face_encoding)

    cursor.execute(
        """
        INSERT INTO users (name, face_encoding)
        VALUES (?, ?)
        """,
        (name, encoding_json)
    )

    conn.commit()
    user_id = cursor.lastrowid

    conn.close()

    return user_id


def get_all_users():
    """
    Get all registered users.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        """
    )

    users = cursor.fetchall()

    conn.close()

    return users


def get_user_by_id(user_id):
    """
    Get user by ID.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user