from contextlib import contextmanager
import sqlite3

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path

    @contextmanager
    def db_connect(self):
        conn = None
        try:
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
