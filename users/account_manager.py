from abc import ABC, abstractmethod

class AccountManager(ABC):

    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def add_user(self):
        pass

    @abstractmethod
    def display_all_users(self):
        pass