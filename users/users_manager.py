import logging
from data.db_config import DBManager
from users.account_manager import AccountManager

class UserManager(AccountManager):
    def __init__(self, db_path):
        self.db_path = db_path
        self.db_manager = DBManager(db_path)
        self.init_db()

    def init_db(self):
        with self.db_manager.db_connect() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(30) NOT NULL UNIQUE
            )''')
        logging.info("Table des utilisateurs initialisée.")

    def add_user(self, name: str) -> None:
        with self.db_manager.db_connect() as cursor:
            cursor.execute("INSERT INTO users (username) VALUES (?)", (name,))
        logging.info(f"Utilisateur ajouté : {name}")
        print(f"Utilisateur '{name}' ajouté.")

    def display_all_users(self) -> str:
        with self.db_manager.db_connect() as cursor:
            cursor.execute("SELECT id, username FROM users")
            users = cursor.fetchall()
            for user in users:
                print(f"User ID: {user[0]} - Nom: {user[1]}")
