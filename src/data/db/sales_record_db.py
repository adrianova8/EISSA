import sqlite3
from src.utils.common.paths import ProjectPaths

paths = ProjectPaths()

DB_NAME = f"{paths.database_dir}/sales.db"

def create_sales_table():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                amount REAL NOT NULL,
                method TEXT NOT NULL
            )
        ''')
        conn.commit()

def insert_sale(date: str, time: str, amount: float, method: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sales (date, time, amount, method)
            VALUES (?, ?, ?, ?)
        ''', (date, time, amount, method))
        conn.commit()

def get_sales_by_date(date: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, time, amount, method FROM sales
            WHERE date = ?
            ORDER BY time ASC
        ''', (date,))
        return cursor.fetchall()
