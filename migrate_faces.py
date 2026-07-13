import sqlite3


conn = sqlite3.connect("database/attendance.db")
cursor = conn.cursor()


# Get old face encodings
cursor.execute("""
SELECT id, face_encoding
FROM users
WHERE face_encoding IS NOT NULL
""")


users = cursor.fetchall()


for user_id, encoding in users:

    # Check if already migrated
    cursor.execute(
        """
        SELECT id
        FROM face_encodings
        WHERE user_id = ?
        """,
        (user_id,)
    )

    exists = cursor.fetchone()


    if exists:
        print(f"User {user_id} already migrated")
        continue


    cursor.execute(
        """
        INSERT INTO face_encodings
        (user_id, encoding)

        VALUES (?, ?)
        """,
        (
            user_id,
            encoding
        )
    )


    print(
        f"Migrated user ID: {user_id}"
    )


conn.commit()
conn.close()


print("Migration completed")