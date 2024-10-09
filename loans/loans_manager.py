import logging
from data.db_config import DBManager

class LoanManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db_manager = DBManager(db_path)
        self.init_db()

    def init_db(self):
        with self.db_manager.db_connect() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                return_date DATETIME,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (book_id) REFERENCES books (id)
            )''')
        logging.info("Table des prêts initialisée.")

    def loan_book(self, user_name: str, book_title: str):
        with self.db_manager.db_connect() as cursor:
            cursor.execute("SELECT id FROM users WHERE username = ?", (user_name,))
            user = cursor.fetchone()
            cursor.execute("SELECT id, available FROM books WHERE title = ?", (book_title,))
            book = cursor.fetchone()

            if user and book:
                if book[1]:
                    cursor.execute("INSERT INTO loans (user_id, book_id) VALUES (?, ?)", (user[0], book[0]))
                    cursor.execute("UPDATE books SET available = ? WHERE id = ?", (False, book[0]))
                    logging.info(f"Livre emprunté : {book_title} par {user_name}")
                    print(f"Livre '{book_title}' emprunté par {user_name}.")
                else:
                    print(f"Le livre '{book_title}' n'est pas disponible.")
            else:
                print("Utilisateur ou livre non trouvé.")

    def return_book(self, user_name: str, book_title: str):
        with self.db_manager.db_connect() as cursor:
            cursor.execute("SELECT id FROM users WHERE username = ?", (user_name,))
            user = cursor.fetchone()
            cursor.execute("SELECT id FROM books WHERE title = ?", (book_title,))
            book = cursor.fetchone()

            if user and book:
                cursor.execute("SELECT id FROM loans WHERE user_id = ? AND book_id = ?", (user[0], book[0]))
                loan = cursor.fetchone()
                if loan:
                    cursor.execute("DELETE FROM loans WHERE id = ?", (loan[0],))
                    cursor.execute("UPDATE books SET available = ? WHERE id = ?", (True, book[0]))
                    logging.info(f"Livre rendu : {book_title} par {user_name}")
                    print(f"Livre '{book_title}' rendu par {user_name}.")
                else:
                    print(f"L'utilisateur '{user_name}' n'a pas emprunté le livre '{book_title}'.")
            else:
                print("Utilisateur ou livre non trouvé.")

    def list_user_loans(self, user_name: str):
        with self.db_manager.db_connect() as cursor:
            cursor.execute("SELECT id FROM users WHERE username = ?", (user_name,))
            user = cursor.fetchone()
            if user:
                cursor.execute('''SELECT b.title, b.author FROM loans l
                                  JOIN books b ON l.book_id = b.id
                                  WHERE l.user_id = ?''', (user[0],))
                loans = cursor.fetchall()
                if loans:
                    print(f"Emprunts de {user_name} :")
                    for loan in loans:
                        print(f"- {loan[0]} par {loan[1]}")
                else:
                    print(f"{user_name} n'a pas d'emprunts en cours.")
            else:
                print(f"Utilisateur '{user_name}' non trouvé.")

    def display_all_loans(self):
        with self.db_manager.db_connect() as cursor:
            cursor.execute('''SELECT u.username, b.title, b.author, l.loan_date FROM loans l
                              JOIN users u ON l.user_id = u.id
                              JOIN books b ON l.book_id = b.id''')
            loans = cursor.fetchall()
            for loan in loans:
                print(f"Utilisateur : {loan[0]} - Livre : {loan[1]} par {loan[2]} - Date de prêt : {loan[3]}")
