# coding=utf-8
class User:
    """Класс User - пользователь, студент, имеющий основные данные:
     ФИ студента-NameOfStudent
     Его группа-GroupOfStudent
     Email
     Является ли он зарегистрированным-IsRegistered"""
    NameOfStudent = ""
    GroupOfStudent = ""
    Email = ""
    IsRegistered = False

    def __init__(self, name=None, group=None, mail=None, registered=None):
        """Конструктор, все входные данные не обязательны для того,
         чтобы была возможность сделать пустой экземпляр класса"""
        self.NameOfStudent = name
        self.GroupOfStudent = group
        self.Email = mail
        self.IsRegistered = registered
