import sqlite3
import logging
from contextlib import contextmanager

class UserManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def db_connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            yield cursor
        except sqlite3.OperationalError as e:
            logging.error(f"Erreur lors de la connexion à la base de données : {e}")
            raise
        finally:
            if conn:
                conn.commit()
                conn.close()


    def init_db(self):
        with self.db_connect() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(30) NOT NULL UNIQUE
            )''')
        logging.info("Table des utilisateurs initialisée.")

    def add_user(self, name: str) -> None:
        with self.db_connect() as cursor:
            cursor.execute("INSERT INTO users (username) VALUES (?)", (name,))
        logging.info(f"Utilisateur ajouté : {name}")
        print(f"Utilisateur '{name}' ajouté.")

    def display_all_users(self) -> str:
        with self.db_connect() as cursor:
            cursor.execute("SELECT id, username FROM users")
            users = cursor.fetchall()
            for user in users:
                print(f"User ID: {user[0]} - Nom: {user[1]}")
