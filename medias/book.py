from medias.IMedia import IMedia  

class Book(IMedia):
    def __init__(self, title, author):
        super().__init__(title, author)
        self.is_available = True

    def __str__(self):
        return f"'{self.title}' par {self.author}"

    def set_available(self, available):
        self.is_available = available

    def is_media_available(self):
        return self.is_available