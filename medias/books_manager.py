# medias/book_manager.py
from data.db_config import DBManager
from medias.medias_manager import IMediasManager
from medias.book import Book
import logging

class BookManager(IMediasManager):
    def __init__(self, db_path):
        self.db_manager = DBManager(db_path)
        self.init_db()

    def init_db(self):
        with self.db_manager.db_connect() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(100) NOT NULL,
                author VARCHAR(100) NOT NULL,
                available BOOLEAN NOT NULL DEFAULT TRUE
            )''')
        logging.info("Table des livres initialisée.")

    def add_media(self):
        title = input("Entrez le titre du livre: ")
        author = input("Entrez l'auteur du livre: ")
        book = Book(title, author)
        with self.db_manager.db_connect() as cursor:
            cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (book.title, book.author))
        logging.info(f"Livre ajouté : {book.title} par {book.author}")
        print(f"Livre '{book.title}' ajouté.")

    def suppr_media(self):
        media_to_suppr = input("Entrez le titre du livre à supprimer: ")
        with self.db_manager.db_connect() as cursor:
            cursor.execute("DELETE FROM books WHERE title = ?", (media_to_suppr,))
        logging.info(f"Livre supprimé : {media_to_suppr}")
        print(f"Livre '{media_to_suppr}' supprimé.")

    def list_available_medias(self):
        with self.db_manager.db_connect() as cursor:
            cursor.execute("SELECT title, author FROM books WHERE available = TRUE")
            available_books = cursor.fetchall()
            for book in available_books:
                print(f"- {book[0]} par {book[1]}")

    def display_all_medias(self):
        with self.db_manager.db_connect() as cursor:
            cursor.execute("SELECT id, title, author FROM books")
            books = cursor.fetchall()
            for book in books:
                print(f"Livre ID: {book[0]} - {book[1]} par {book[2]}")
