import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "shopping.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            results TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_search(query, results_json):
    conn = get_connection()
    conn.execute("INSERT INTO searches (query, results) VALUES (?, ?)", (query, results_json))
    conn.commit()
    conn.close()

def get_all_searches():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM searches ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]