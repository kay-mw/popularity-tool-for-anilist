import sqlite3


def init_db(DATABASE_NAME):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        insights TEXT
    )
    """
    )
    conn.commit()
    conn.close()
