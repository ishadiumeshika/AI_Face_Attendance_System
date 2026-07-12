import sqlite3
from datetime import datetime
from pathlib import Path

DATABASE_PATH = Path("database/attendance.db")


def create_database():
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Student information table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        face_encoding TEXT NOT NULL
    )
    """)

    # Attendance table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def add_student(student_id, name, face_encoding):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students(student_id, name, face_encoding)
    VALUES (?, ?, ?)
    """,
    (student_id, name, face_encoding))

    conn.commit()
    conn.close()


def get_students():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    conn.close()

    return data


def mark_attendance(student_id, name):
    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO attendance(student_id, name, date, time)
    VALUES (?, ?, ?, ?)
    """,
    (student_id, name, date, time))

    conn.commit()
    conn.close()


def get_attendance():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM attendance
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data