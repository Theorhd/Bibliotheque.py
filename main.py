import os
from data.db_config import DBManager
from users.users_manager import UserManager
from medias.books_manager import BookManager
from loans.loans_manager import LoanManager

class LibraryApp:
    def __init__(self, db_path):
        self.db_manager = DBManager(db_path)
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
            '1': lambda: self.book_manager.add_media(),
            '2': lambda: self.user_manager.add_user(input("Nom de l'utilisateur : ")),
            '3': lambda: self.loan_manager.loan_book(input("Nom de l'utilisateur : "), input("Titre du livre à emprunter : ")),
            '4': lambda: self.loan_manager.return_book(input("Nom de l'utilisateur : "), input("Titre du livre à rendre : ")),
            '5': self.book_manager.list_available_medias,
            '6': lambda: self.loan_manager.list_user_loans(input("Nom de l'utilisateur : ")),
            '7': self.user_manager.display_all_users,
            '8': self.book_manager.display_all_medias,
            '9': self.loan_manager.display_all_loans,
            '10': lambda: self.book_manager.suppr_media(),
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
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.sqlite3')
    app = LibraryApp(db_path)
    app.main()
