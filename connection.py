import os

import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager
load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")



def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


@contextmanager
def get_connection():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()