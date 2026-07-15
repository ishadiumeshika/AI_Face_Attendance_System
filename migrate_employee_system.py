import sqlite3
import random


DB = "database/attendance.db"


conn = sqlite3.connect(DB)

cursor = conn.cursor()


# Add employee_id

try:

    cursor.execute(
        """
        ALTER TABLE users
        ADD COLUMN employee_id TEXT
        """
    )

except:

    pass



# Add email

try:

    cursor.execute(
        """
        ALTER TABLE users
        ADD COLUMN email TEXT
        """
    )

except:

    pass



# Create unique email index

try:

    cursor.execute(
        """
        CREATE UNIQUE INDEX idx_email
        ON users(email)
        """
    )

except:

    pass



# Generate employee IDs for old users

cursor.execute(
    """
    SELECT id
    FROM users
    WHERE employee_id IS NULL
    """
)


users = cursor.fetchall()


for user in users:

    emp_id = "EMP" + str(1000 + user[0])


    cursor.execute(
        """
        UPDATE users
        SET employee_id = ?
        WHERE id = ?
        """,
        (
            emp_id,
            user[0]
        )
    )



conn.commit()

conn.close()


print("Employee system migration completed")