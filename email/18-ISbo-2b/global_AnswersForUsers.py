# coding=utf-8
class AnswersForUsers:
    """класс AnswersForUsers-ответы пользователям, содержит данные:
    Кому написано - Who
    Тема письма - Theme
    Что написано - Body
    """
    Who = ""
    Theme = ""
    Body = ""

    def __init__(self, who=None, theme=None, body=None):
        """Конструктор, все входные данные не обязательны для того,
                 чтобы была возможность сделать пустой экземпляр класса"""
        self.Who = who
        self.Theme = theme
        self.Body = body
