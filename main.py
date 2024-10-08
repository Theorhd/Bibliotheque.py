import os
from users.users_manager import UserManager
from books.books_manager import BookManager
from loans.loans_manager import LoanManager

class LibraryApp:
    def __init__(self, db_path):
        # Vérifiez si le dossier parent existe, sinon créez-le
        db_folder = os.path.dirname(db_path)
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)

        self.user_manager = UserManager(db_path)
        self.book_manager = BookManager(db_path)
        self.loan_manager = LoanManager(db_path)

    def afficher_menu(self):
        print("""
            =============== MENU ===============
            1. Ajouter un livre
            2. Ajouter un utilisateur
            3. Emprunter un livre
            4. Rendre un livre
            5. Lister les livres disponibles
            6. Lister les emprunts d'un utilisateur
            7. Afficher tous les users
            8. Afficher tous les livres
            9. Afficher tous les emprunts
            10. Supprimer un livre
            0. Quitter
            =====================================
          """)

    def obtenir_choix_utilisateur(self):
        choix = input("Veuillez entrer votre choix (0-10) : ")
        return choix

    def main(self):
        actions = {
            '1': lambda: self.book_manager.add_book(input("Titre du livre : "), input("Auteur du livre : ")),
            '2': lambda: self.user_manager.add_user(input("Nom de l'utilisateur : ")),
            '3': lambda: self.loan_manager.loan_book(input("Nom de l'utilisateur : "), input("Titre du livre à emprunter : ")),
            '4': lambda: self.loan_manager.return_book(input("Nom de l'utilisateur : "), input("Titre du livre à rendre : ")),
            '5': self.book_manager.list_available_books,
            '6': lambda: self.loan_manager.list_user_loans(input("Nom de l'utilisateur : ")),
            '7': self.user_manager.display_all_users,
            '8': self.book_manager.display_all_books,
            '9': self.loan_manager.display_all_loans,
            '10': lambda: self.book_manager.suppr_book(input("Titre du livre à supprimer : ")),
        }

        while True:
            self.afficher_menu()
            choix = self.obtenir_choix_utilisateur()

            if choix == '0':
                print("Fin du programme.")
                break
            elif choix in actions:
                actions[choix]()
            else:
                print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    dossier_actuel = os.path.dirname(__file__)
    chemin_db = os.path.join(dossier_actuel, 'data', 'app.sqlite3')
    app = LibraryApp(chemin_db)
    app.main()
