# coding=utf-8
class LetterResult:
    """Класс LetterResult-результат письма, содержит данные:
    Студент-Student, при помощи класса User,
    Тема письма-ThemeOfLetter
    Является ли решение правильным-IsOK
    Вариант лабораторной работы - Variant
    Статусы-CodeStatus, CodeStatusComment"""
    Student = None    
    IsOK = False
    Comment = ""
    VariantOfLab = 0
    NumberOfLab = 0
    CodeStatus = "0"
    CodeStatusComment = ""

    def __init__(self, student=None, isOK=None, variant=None, number=None):
        """Конструктор, все входные данные не обязательны для того,
         чтобы была возможность сделать пустой экземпляр класса"""
        self.Student = student
        self.IsOK = isOK
        self.VariantOfLab = variant
        self.NumberOfLab = number
