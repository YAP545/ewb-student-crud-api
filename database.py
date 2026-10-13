import os
import sqlite3
from typing import Generator

DB_FILE_PATH = os.environ.get("STUDENT_DB_PATH", "students.db")

def get_connection(db_path: str = None) -> sqlite3.Connection:
    target_path = db_path or os.environ.get("STUDENT_DB_PATH", "students.db")
    conn = sqlite3.connect(target_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(db_path: str = None) -> None:
    conn = get_connection(db_path)
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    date_of_birth TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    course TEXT,
                    address TEXT,
                    enrollment_date TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    finally:
        conn.close()

def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
