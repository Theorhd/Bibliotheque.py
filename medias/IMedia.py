from abc import ABC, abstractmethod

class IMedia(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def is_media_available(self):
        pass

    @abstractmethod
    def set_available(self, available):
        pass