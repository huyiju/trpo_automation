import User


class Letter:
    """Класс Letter-письмо, содержит данные:
    Студент-Student, при помощи класса User,
    Тема письма-ThemeOfLetter
    Его содержание-Body
    Статусы-CodeStatus, CodeStatusComment"""
    Student = User.User()
    ThemeOfLetter = ""
    Body = object()
    CodeStatus = 0
    CodeStatusComment = ""

    def __init__(self, student=None, themeOfLetter=None, body=None, codeStatus=None, codeStatusComment=None):
        """Конструктор, все входные данные не обязательны для того,
         чтобы была возможность сделать пустой экземпляр класса"""
        self.Student = student
        self.ThemeOfLetter = themeOfLetter
        self.Body = body
        self.CodeStatus = codeStatus
        self.CodeStatusComment = codeStatusComment
