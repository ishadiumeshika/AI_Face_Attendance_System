import sqlite3


DB = "database/attendance.db"


conn = sqlite3.connect(DB)

cursor = conn.cursor()


# Delete attendance records

cursor.execute(
    "DELETE FROM attendance"
)


# Delete face encodings

cursor.execute(
    "DELETE FROM face_encodings"
)


# Delete users

cursor.execute(
    "DELETE FROM users"
)


conn.commit()


conn.close()


print("All users, faces and attendance records deleted")