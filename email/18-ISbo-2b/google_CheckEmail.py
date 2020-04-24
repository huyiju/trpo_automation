# coding=utf-8
from time import sleep
from datetime import datetime

from global_Letter import Letter
from global_User import User
from base_WorkWithLetters import WorkWithLetters
import config as cfg

def CheckEmail():
    """
    Точка входа в работу модуля.
    Чтение писем, их парсинг и валидация.
    """

    letters = GetLetters()

    cfg.timer.SetTimer()

    cfg.reserve_dates.GetReserveDate()


    letters = FormListWithLetters(letters)

    CheckUsers(letters)

    ValidateLetters(letters)

    WorkWithLetters(letters)


def GetLetters():
    """
   Функционал:
   - Прочитать письма на почте
   - Пометить прочитанные письма метками
   На входе:
   - None
   На выходе:
   - letters - объект, содержащий письма
   Что предусмотреть:
   - None
   Участвующие внешние типы переменных
   - None
   """
    with open(cfg.filename, "a") as file: file.write("\nGetting letters...")
    letters = ["letter1", "letter2", "letter3"]
    sleep(1)
    with open(cfg.filename, "a") as file: file.write("Letters gets!")
    return letters

def FormListWithLetters(letters):
    """
    Функционал:
    - Сформировать список экземпляров класса Letter на основе сырых данных по письмам
    На входе:
    - Объект с сырыми данными по письмам
    На выходе:
    - Список экземпляров класса Letter
    Что предусмотреть:
    - Парсинг сырых данных
    - Декодирование сырых данных
    - Заполнение всех полей в Letter на основе обработанной информации кроме 'Code' и 'CodeComment'
    - Поля 'Code' и 'CodeComment' заполняются только в случае существующего приложения к письму (что противоречит
    правилам отправки писем)
    - Заполнение поля User - вытаскивание всех данных о конкретном пользователе (кроме поля isRegistered)
    Участвующие внешние типы переменных
    - User (from import)
    - Letter (from import)
    """
    with open(cfg.filename, "a") as file: file.write("\nForming letters...")
    sleep(1)
    new_letters = []
    for i in letters:
        user = User()
        letter = Letter(user)
        new_letters.append(letter)
    with open(cfg.filename, "a") as file: file.write("Letters forms!")

    return new_letters


def CheckUsers(letters):
    """
    Функционал:
    - Проверить зарегистрированность каждого пользователя в системе по email
    На входе:
    - Список писем
    На выходе:
    - Расставленное поле 'isRegistered' в каждом письме в поле 'User'
    Что предусмотреть:
    - None
    Участвующие внешние типы переменных
    - None
    """
    with open(cfg.filename, "a") as file: file.write ("\nChecking users...")
    for i in letters:
        i.Student.IsRegistered = True
    sleep(1)
    with open(cfg.filename, "a") as file: file.write("Users cheks!")

def ValidateLetters(letters):
    """
    Функционал:
    - Провалидировать каждое письмо по правилам валидации
    На входе:
    - Список писем
    На выходе:
    - Расставленные поля 'Code' и 'CodeComment' в каждом письме
    Что предусмотреть:
    - Просле проверки вытащить ссылки на ресурсы и поместить их в поле 'Body' каждого письма
    - Проверку выполнять только если поле 'Code' ещё не заполнено
    - Поле 'CodeComment' заполнять сокращённой информацией по результатам проверки как угодно.
    Участвующие внешние типы переменных
    - None
    """
    with open(cfg.filename, "a") as file: file.write("\nValidating letters...")
    for i in letters:
        i.CodeStatus = 20
        i.CodeStatusComment = "All is good"
    sleep(1)
    with open(cfg.filename, "a") as file: file.write("Letters validates!")
