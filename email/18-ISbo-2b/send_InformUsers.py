# coding=utf-8
from time import sleep
from datetime import datetime
from email.message import EmailMessage

import config as cfg
import config_email
import smtplib
import email

def InformUsers(answersForUsers):
    """
    Разослать письма пользователям, внести пользователей в список, заархивировать письма, дождаться таймера
    """
    smtp_obj = smtp_login()
    SendLetters(smtp_obj, answersForUsers)
    quit_email_smtp(smtp_obj)

    ArchiveLetters()

    AddUsers()

    cfg.timer.WaitForTimer()

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
    for i in answersForUsers:
        send_mes(smtp_obj, i)


def send_mes(smtp_obj, message):
    try:
        with open(cfg.filename, "a") as file:
            file.write("\nSetting letter for users...")
        sleep(1)
        mes = EmailMessage()
        mes['From'] = "ТРПО ИАСТ"
        mes['To'] = message.Who
        mes['Subject'] = message.Theme
        mes.set_content(message.Body)
        smtp_obj.send_message(mes)
        with open(cfg.filename, "a") as file:
            file.write("\nLetter send!")
    except:
        with open(cfg.filename, "a") as file:
            file.write("\nSending message error!")

def ArchiveLetters():
    """
     Функционал:
    - Заархивировать отмеченные письма
    На входе:
    - None
    На выходе:
    - None
    Что предусмотреть:
    - None
    Участвующие внешние типы переменных
    - None
    """
    with open(cfg.filename, "a") as file: file.write("\nArchiving letters...")
    sleep(1)
    with open(cfg.filename, "a") as file: file.write("Letters archived!")

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
    with open(cfg.filename, "a") as file: file.write("\nAdding users...")
    sleep(1)
    with open(cfg.filename, "a") as file: file.write("Users add!")

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
    smtpObj.login(config_email.EMAIL_ADDRESS, config_email.EMAIL_PASSWORD)
    return smtpObj

def quit_email_smtp(smtpObj):
    """
    Закрытие SMTP объекта.
    Функция должна быть вызвана после завершения рыботы с SMTP объектом.
    :param smtpObj:
    :return:
    """
    smtpObj.close()
