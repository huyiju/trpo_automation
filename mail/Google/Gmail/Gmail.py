import smtplib
from email.message import EmailMessage
import config
import imaplib


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
    smtpObj.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
    return smtpObj


def imap_login():
    """
    Авторизация в Gmail аккаунте.
    Функция возвращает IMAP объект.
    :return:
    """
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
    imap.select('inbox')
    return imap


def quit_email_smtp(smtpObj):
    """
    Закрытие SMTP объекта.
    Функция должна быть вызвана после завершения рыботы с SMTP объектом.
    :param smtpObj:
    :return:
    """
    smtpObj.close()


def quit_email_smtp(imapObj):
    """
    Закрытие IMAP объекта.
    Функция должна быть вызвана после завершения рыботы с SMTP объектом.
    :param imapObj:
    :return:
    """
    imapObj.close()


def send_mess(smtpObj, mailTo, topic, text):
    """
    Функция для отправки сообщения.
    :param smtpObj:
    :param mailTo:
    :param topic:
    :param text:
    :return:
    """
    mes = EmailMessage()
    mes['From'] = "ТРПО ИАСТ"
    mes['To'] = mailTo
    mes['Subject'] = topic
    mes.set_content(text)
    smtpObj.send_message(mes)


def count_unseen_mess(mail):
    """
    Возвращает кол-во непрочитанных сообщений
    :param mail:
    :return:
    """
    result, data = mail.uid('search', None, "unseen")
    return len(data[0].split())


def read(mail):
    """
    Функция считывающая новые gmail сообщения
    :param mail:
    :return:
    """
    count = count_unseen_mess(mail)
    if count > 0:
        return_result = []
        result, data = mail.uid('search', None, "unseen")  # Выполняет поиск и возвращает UID писем.
        print(count)
        for i in range(count):
            latest_email_uid = data[0].split()[i]
            result, date = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = date[0][1]
            return_result.append(raw_email)
            print("ready")
        return return_result
    else:
        print("Отсутствие новых сообщений.")
