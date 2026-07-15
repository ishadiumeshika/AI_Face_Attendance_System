import sqlite3


DB_PATH = "database/attendance.db"


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# Add username column
try:
    cursor.execute(
        """
        ALTER TABLE users
        ADD COLUMN username TEXT
        """
    )
except sqlite3.OperationalError:
    pass


# Add password column
try:
    cursor.execute(
        """
        ALTER TABLE users
        ADD COLUMN password TEXT
        """
    )
except sqlite3.OperationalError:
    pass


# Add role column
try:
    cursor.execute(
        """
        ALTER TABLE users
        ADD COLUMN role TEXT DEFAULT 'Employee'
        """
    )
except sqlite3.OperationalError:
    pass



# Create unique index for usernames
try:
    cursor.execute(
        """
        CREATE UNIQUE INDEX idx_users_username
        ON users(username)
        """
    )
except sqlite3.OperationalError:
    pass



# Check manager account
cursor.execute(
    """
    SELECT id
    FROM users
    WHERE username = ?
    """,
    ("manager",)
)


manager = cursor.fetchone()


if manager is None:

    cursor.execute(
        """
        INSERT INTO users
        (
            name,
            username,
            password,
            role
        )

        VALUES (?, ?, ?, ?)
        """,
        (
            "System Manager",
            "manager",
            "admin123",
            "Manager"
        )
    )


conn.commit()
conn.close()


print("Login fields added successfully")