import os
from contextlib import contextmanager
import sqlite3

class DBManager:
    def __init__(self, db_path):
        # Utiliser le chemin de base de données fourni lors de l'instanciation
        self.db_path = db_path

    @contextmanager
    def db_connect(self):
        conn = None
        try:
            # Établir une connexion à la base de données en utilisant le chemin spécifié
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            yield cursor
        except sqlite3.OperationalError as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")
            raise
        finally:
            if conn:
                conn.commit()
                conn.close()
