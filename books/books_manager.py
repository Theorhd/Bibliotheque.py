import sqlite3
import logging
from contextlib import contextmanager

class BookManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def db_connect(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            yield cursor
        finally:
            conn.commit()
            conn.close()

    def init_db(self):
        with self.db_connect() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(100) NOT NULL,
                author VARCHAR(100) NOT NULL,
                available BOOLEAN NOT NULL DEFAULT TRUE
            )''')
        logging.info("Table des livres initialisée.")

    def add_book(self, title: str, author: str):
        with self.db_connect() as cursor:
            cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        logging.info(f"Livre ajouté : {title} par {author}")
        print(f"Livre '{title}' ajouté.")

    def suppr_book(self, title: str):
        with self.db_connect() as cursor:
            cursor.execute("DELETE FROM books WHERE title = ?", (title,))
        logging.info(f"Livre supprimé : {title}")
        print(f"Livre '{title}' supprimé.")

    def list_available_books(self):
        with self.db_connect() as cursor:
            cursor.execute("SELECT title, author FROM books WHERE available = TRUE")
            available_books = cursor.fetchall()
            for book in available_books:
                print(f"- {book[0]} par {book[1]}")

    def display_all_books(self):
        with self.db_connect() as cursor:
            cursor.execute("SELECT id, title, author FROM books")
            books = cursor.fetchall()
            for book in books:
                print(f"Livre ID: {book[0]} - {book[1]} par {book[2]}")
