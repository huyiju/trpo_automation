# coding=utf-8
from time import sleep
from datetime import datetime
from email import *
from global_Letter import Letter
from global_User import User
from base_WorkWithLetters import WorkWithLetters
from google_ValidateRules import ValidationMail as Val
import config as cfg
<<<<<<< HEAD
import re


=======
from email.message import EmailMessage
import config_email
import imaplib
import email
import base64
>>>>>>> issue-257

def CheckEmail():
    """
    Точка входа в работу модуля.
    Чтение писем, их парсинг и валидация.
    """
    imap_obj = imap_login()
    letters = GetLetters(imap_obj)
    quit_email_imap(imap_obj)

    cfg.timer.SetTimer()

    cfg.reserve_dates.GetReserveDate()

    letters = FormListWithLetters(letters)

    CheckUsers(letters)

    ValidateLetters(letters)

    WorkWithLetters(letters)


def GetLetters(mail):
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
<<<<<<< HEAD
    with open(cfg.filename, "a") as file: file.write("\nGetting letters...")
    letters = ["letter1", "letter2", "letter3"]
    sleep(1)
    with open(cfg.filename, "a") as file: file.write("Letters gets!")
    return letters


=======
    count = count_unseen_mess(mail)
    if count > 0:
        letters = []
        result, data = mail.uid('search', None, "unseen")  # Выполняет поиск и возвращает UID писем.
        print(count)
        for i in range(count):
            latest_email_uid = data[0].split()[i]
            result, date = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = date[0][1]
            letters.append(raw_email)
        with open(cfg.filename, "a") as file:
            file.write("\nGetting letters...")
        letters = ["letter1", "letter2", "letter3"]
        sleep(1)
        with open(cfg.filename, "a") as file:
            file.write("Letters gets!")
        return letters
    else:
        print("Отсутствие новых сообщений.")
>>>>>>> issue-257
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
    with open(cfg.filename, "a") as file: file.write("\nChecking users...")
    for i in letters:
        i.Student.IsRegistered = True
    sleep(1)
    with open(cfg.filename, "a") as file: file.write("Users cheks!")


def ValidateLetters(letters):
<<<<<<< HEAD
    for let in letters:
        if let.CodeStatus is None:
            val = Val(let.ThemeOfLetter, let.Body)
            let.CodeStatus = val.validation(val.subject, val.body)
            if let.CodeStatus == '02':
                let.CodeStatusComment = 'Структура письма не соответствует требованиям к оформлению'
            elif let.CodeStatus == '03':
                let.CodeStatusComment = 'Номер варианта меньше 1 или больше 15 или не число'
            else:
                num, var = val.get_num_and_var(val.subject)
                if int(num) < 1 or int(num) > 15 or int(var) == 0:
                    let.CodeStatus = '03'
                    let.CodeStatusComment = 'Номер лабораторной не существует'
                else:
                    let.Number = var
                    let.Variant = num
            if let.CodeStatus == '20':
                let.Body = re.findall(r'http[^ \n]*', let.Body)
                let.CodeStatusComment = 'Работа отправлена на проверку'
=======
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

def imap_login():
    """
    Авторизация в Gmail аккаунте.
    Функция возвращает SMTP объект.
    :return:
    """
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(config_email.EMAIL_ADDRESS, config_email.EMAIL_PASSWORD)
    imap.select('inbox')
    return imap

def quit_email_imap(imapObj):
    """
    Закрытие SMTP объекта.
    Функция должна быть вызвана после завершения рыботы с SMTP объектом.
    :param smtpObj:
    :return:
    """
    imapObj.close()

def count_unseen_mess(mail):
    """
    Возвращает кол-во непрочитанных сообщений
    :param mail:
    :return:
    """
    result, data = mail.uid('search', None, "unseen")
    return len(data[0].split())
>>>>>>> issue-257
