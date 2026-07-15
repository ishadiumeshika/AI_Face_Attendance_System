import sqlite3
import json

from app.database.db_connection import get_connection

def add_user(name, email, password):
    """
    Add a new employee.
    """

    conn = get_connection()
    cursor = conn.cursor()
    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password
            )

            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                password
            )
        )


        conn.commit()


        


        return user_id


    except sqlite3.IntegrityError as e:

        conn.rollback()


        error_message = str(e)


        if "email" in error_message:

            return "EMAIL_EXISTS"


        

        return "ERROR"


    finally:

        conn.close()
    # Check if email already exists

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    existing = cursor.fetchone()

    if existing:

        conn.close()

        raise Exception(
            "Email already registered"
        )


    # Generate Employee ID

    cursor.execute(
        """
        SELECT id
        FROM users
        ORDER BY id DESC
        LIMIT 1
        """
    )

    last = cursor.fetchone()


    if last:

        employee_id = (
            "EMP"
            + str(
                1000 + last["id"] + 1
            )
        )

    else:

        employee_id = "EMP1001"


    # Insert new user

    cursor.execute(
        """
        INSERT INTO users
        (
            employee_id,
            name,
            email,
            password,
            role
        )

        VALUES (?, ?, ?, ?, ?)
        """,
        (
            employee_id,
            name,
            email,
            password,
            "Employee"
        )
    )


    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return user_id, employee_id
def get_all_users():
    """
    Return every face encoding together with user details.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            users.id,
            users.name,
            users.employee_id,
            users.email,
            face_encodings.encoding

        FROM users

        JOIN face_encodings
        ON users.id = face_encodings.user_id
        """
    )

    users = cursor.fetchall()

    conn.close()

    return users
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
def add_face_encoding(user_id, face_encoding):

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

def get_user_by_id(user_id):

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
def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        AND password = ?
        """,
        (
            email,
            password
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user
def delete_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM face_encodings WHERE user_id=?",
        (user_id,)
    )

    cursor.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()