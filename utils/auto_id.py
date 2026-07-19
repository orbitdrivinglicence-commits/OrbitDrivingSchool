import sqlite3

DB_PATH = "database/database.db"


def generate_registration_id():
    """
    Generates Registration ID like:
    ORB0001
    ORB0002
    ORB0003
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT registration_id
        FROM students
        ORDER BY registration_id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return "ORB0001"

    last_id = row[0]

    try:
        number = int(last_id.replace("ORB", ""))
    except ValueError:
        number = 0

    number += 1

    return f"ORB{number:04d}"


if __name__ == "__main__":
    print(generate_registration_id())
