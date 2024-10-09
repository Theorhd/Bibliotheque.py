from abc import ABC, abstractmethod

class IMedia(ABC):
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True
        
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def is_media_available(self):
        pass

    @abstractmethod
    def set_available(self, available):
        pass