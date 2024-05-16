import sqlite3
from flask import g

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.db_name)
        return db

    def close_connection(self, exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    def create_table(self):
        with self.get_db() as conn:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    company TEXT,
                    phone TEXT,
                    email TEXT
                )
            ''')
            conn.commit()

    def add_customer(self, name, company, phone, email):
        with self.get_db() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO customers (name, company, phone, email) VALUES (?, ?, ?, ?)", (name, company, phone, email))
            conn.commit()

    def get_all_customers(self):
        with self.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM customers")
            return cur.fetchall()
