import sqlite3


DB_PATH = "database/attendance.db"


conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS leave_requests
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        reason TEXT NOT NULL,

        from_date TEXT NOT NULL,

        to_date TEXT NOT NULL,

        status TEXT DEFAULT 'Pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


        FOREIGN KEY(user_id)
        REFERENCES users(id)
    )
    """
)


conn.commit()

conn.close()


print("Leave table created successfully")