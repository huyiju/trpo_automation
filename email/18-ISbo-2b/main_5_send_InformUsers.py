# coding=utf-8
from time import sleep
from datetime import datetime
from email.message import EmailMessage

import config_Project as cfg
import config_Mail
import smtplib
import email

def InformUsers(answersForUsers):
    """
    Разослать письма пользователям, внести пользователей в список, заархивировать письма, дождаться таймера
    """
    # Отправление писем пользователям
    smtp_obj = smtp_login()
    SendLetters(smtp_obj, answersForUsers)
    quit_email_smtp(smtp_obj)

    # Добавление пользователей (функция пока не реализована)
    AddUsers()

    # Формирование нового имени файла логов
    FormFilename()


def SendLetters(smtp_obj, answersForUsers):
    """
     Функционал:
    - Разослать письма пользователям
    На входе:
    - Сформированный список экземпляров класса AnswersForUsers, где в поле Who находится email пользователя,
    в поле Theme - тема письма, а в поле Body - тело письма
    На выходе:
    - None
    Что предусмотреть:
    - None
    Участвующие внешние типы переменных
    - None
    """

    with open(cfg.filename, "a") as file:
        file.write("\nОтправление ответов пользователю... ")

    for i in answersForUsers:

        mes = EmailMessage()
        mes['From'] = "ТРПО ИАСТ"
        mes['To'] = i.Who
        mes['Subject'] = i.Theme
        mes.set_content(i.Body)
        smtp_obj.send_message(mes)

    with open(cfg.filename, "a") as file:
        file.write("Ответы отправлены!")

def AddUsers():
    """
    Функционал:
    - Добавить в журнал тех пользователей, которые заполнили форму регистрации
    На входе:
    - None
    На выходе:
    - None
    Что предусмотреть:
    - Внести в список только тех, кто заполняет форму регистрации с момента последнего добавления
    Возможно, предусмотреть удаление записей из временного списка после добавления в основной журнал
    Участвующие внешние типы переменных
    - None
    """
    with open(cfg.filename, "a") as file:
        file.write("\nДобавление пользователей... ")

    with open(cfg.filename, "a") as file:
        file.write("Пользователи добавлены!")

def FormFilename():
    """
    Формирование имени файла логов
    """
    name = datetime.strftime(datetime.now(), "%Y.%m.%d")
    if name != cfg.last_date:
        cfg.last_date = name
        cfg.gen_num_for_filename = cfg.num_for_filename()

    cfg.filename = cfg.path_to_logs + "log_" + name + "_" + str(next(cfg.gen_num_for_filename)) + ".txt"

def smtp_login():
    """
    Авторизация в Gmail аккаунте.
    Функция возвращает SMTP объект.
    :return:
    """
    smtpObj = smtplib.SMTP('smtp.gmail.com:587')
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.ehlo()
    smtpObj.login(config_Mail.EMAIL_ADDRESS, config_Mail.EMAIL_PASSWORD)
    return smtpObj

def quit_email_smtp(smtpObj):
    """
    Закрытие SMTP объекта.
    Функция должна быть вызвана после завершения рыботы с SMTP объектом.
    :param smtpObj:
    :return:
    """
    smtpObj.close()
