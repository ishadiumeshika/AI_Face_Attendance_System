import json

from app.database.db_connection import get_connection


def add_user(name):
    """
    Add a new user.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (name)
        VALUES (?)
        """,
        (name,)
    )

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return user_id


def add_face_encoding(user_id, face_encoding):
    """
    Save one face encoding for a user.
    """

    conn = get_connection()
    cursor = conn.cursor()

    encoding_json = json.dumps(face_encoding)

    cursor.execute(
        """
        INSERT INTO face_encodings
        (user_id, encoding)

        VALUES (?, ?)
        """,
        (
            user_id,
            encoding_json
        )
    )

    conn.commit()
    conn.close()


def get_all_users():
    """
    Return every face encoding together with the user's name.
    One user may have multiple encodings.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            users.id,
            users.name,
            face_encodings.encoding

        FROM users

        JOIN face_encodings
        ON users.id = face_encodings.user_id
        """
    )

    users = cursor.fetchall()

    conn.close()

    return users


def get_user_by_id(user_id):
    """
    Get one user by ID.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def get_user_by_name(name):
    """
    Get one user by name.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE LOWER(name) = LOWER(?)
        """,
        (name,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def user_exists(name):
    """
    Check whether a user already exists.
    """

    return get_user_by_name(name) is not None


def delete_user(user_id):
    """
    Delete a user and all of their face encodings.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM face_encodings
        WHERE user_id = ?
        """,
        (user_id,)
    )

    cursor.execute(
        """
        DELETE FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()