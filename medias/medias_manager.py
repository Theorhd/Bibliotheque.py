from abc import ABC, abstractmethod

class IMediasManager(ABC):
    @abstractmethod
    def add_media(self, media):
        pass

    @abstractmethod
    def suppr_media(self, media):
        pass

    @abstractmethod
    def list_available_medias(self):
        pass

    @abstractmethod
    def display_all_medias(self):
        pass