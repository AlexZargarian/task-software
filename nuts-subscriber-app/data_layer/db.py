# data_layer/db.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    # Retrieve database connection details from environment variables.
    db_config = {
        "dbname": os.environ.get("DB_NAME", "nuts_db"),
        "user": os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASSWORD", "your_password"),
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": os.environ.get("DB_PORT", 5432)
    }
    return psycopg2.connect(**db_config, cursor_factory=RealDictCursor)

def save_message(message_dict: dict):
    query = """
    INSERT INTO messages (content, timestamp)
    VALUES (%s, %s);
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (message_dict["content"], message_dict["timestamp"]))
                conn.commit()
        print("Message successfully saved to the database.")
    except Exception as e:
        print("Error saving message:", e)
