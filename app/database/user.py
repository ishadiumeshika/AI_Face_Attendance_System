import sqlite3
import json

from app.database.db_connection import get_connection



# =========================
# ADD USER
# =========================

def add_user(name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Check duplicate email

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

            return "EMAIL_EXISTS"



        # Generate employee ID

     
        cursor.execute(
            """
            SELECT MAX(
                CAST(
                    SUBSTR(employee_id,4) AS INTEGER
                )
            )
            FROM users
            WHERE employee_id LIKE 'EMP%'
            """
        )

        last = cursor.fetchone()[0]


        if last:

            employee_id = f"EMP{last + 1:04d}"

        else:

            employee_id = "EMP1001"



        # Insert user

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


        return user_id



    except Exception as e:

        conn.rollback()

        print(
            "Add user error:",
            e
        )

        return str(e)



    finally:

        conn.close()





# =========================
# GET ALL USERS WITH FACES
# =========================

# =========================
# GET ALL USERS
# =========================

def get_all_users():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            id,
            name,
            employee_id,
            email,
            role

        FROM users
        """
    )


    users = cursor.fetchall()


    conn.close()


    return users





# =========================
# TOTAL EMPLOYEES
# =========================

def get_total_employees():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE role='Employee'
        """
    )


    count = cursor.fetchone()[0]


    conn.close()


    return count





# =========================
# GET USER BY NAME
# =========================

def get_user_by_name(name):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE LOWER(name)=LOWER(?)
        """,
        (name,)
    )


    user = cursor.fetchone()


    conn.close()


    return user





# =========================
# GET USER BY EMAIL
# =========================

def get_user_by_email(email):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email=?
        """,
        (email,)
    )


    user = cursor.fetchone()


    conn.close()


    return user





# =========================
# SAVE FACE ENCODING
# =========================

def add_face_encoding(user_id, face_encoding):

    conn = get_connection()
    cursor = conn.cursor()


    encoding_json = json.dumps(
        face_encoding
    )


    cursor.execute(
        """
        INSERT INTO face_encodings
        (
            user_id,
            encoding
        )

        VALUES (?, ?)
        """,
        (
            user_id,
            encoding_json
        )
    )


    conn.commit()

    conn.close()





# =========================
# GET USER BY ID
# =========================

def get_user_by_id(user_id):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id=?
        """,
        (user_id,)
    )


    user = cursor.fetchone()


    conn.close()


    return user





# =========================
# LOGIN
# =========================

def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email=?
        AND password=?
        """,
        (
            email,
            password
        )
    )


    user = cursor.fetchone()


    conn.close()


    return user





# =========================
# DELETE USER
# =========================

def delete_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()


    # Delete face data first

    cursor.execute(
        """
        DELETE FROM face_encodings
        WHERE user_id=?
        """,
        (user_id,)
    )


    # Delete user

    cursor.execute(
        """
        DELETE FROM users
        WHERE id=?
        """,
        (user_id,)
    )


    conn.commit()

    conn.close()

def fix_missing_employee_ids():

    conn = get_connection()
    cursor = conn.cursor()

    # Find users without employee IDs
    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE employee_id IS NULL
        """
    )

    users = cursor.fetchall()


    # Find current last employee number
    cursor.execute(
        """
        SELECT MAX(
            CAST(SUBSTR(employee_id,4) AS INTEGER)
        )
        FROM users
        WHERE employee_id LIKE 'EMP%'
        """
    )

    last = cursor.fetchone()[0]


    if last:
        next_id = last + 1
    else:
        next_id = 1001



    for user in users:

        employee_id = f"EMP{next_id}"

        cursor.execute(
            """
            UPDATE users
            SET employee_id = ?
            WHERE id = ?
            """,
            (
                employee_id,
                user["id"]
            )
        )

        next_id += 1



    conn.commit()
    conn.close()