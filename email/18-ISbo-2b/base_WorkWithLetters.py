# coding=utf-8
from time import sleep
from datetime import datetime

from global_LetterResult import LetterResult
from send_SetResults import SetResults
import config as cfg

def WorkWithLetters(letters):
    """
    Работа с письмами, формирование правильного формата данных,
    отправка их на проверку, принятие результатов и их передача дальше
    """

    LettersConvertToString(letters)

    jsonDates = FormJSONDates(letters)

    letterResults = SendJSONForCheck(jsonDates, letters)

    # SetResults - Передать данные следующему модулю в формате списка экземпляров класса EmailResults
    SetResults(letterResults)

def LettersConvertToString(letters):
    """
    Функционал:
    - Вытащить сырые данные по ссылкам из поля Body
    - Переконвертировать их в строковой формат и разместить в поле Body
    На входе:
    - letter - заполненный и провалидированный список писем - экземпляров класса Letter
    На выходе:
    - letters - Список писем, в каждом из которых в поле Body лежит необходимая для отправки информация
    Что предусмотреть:
    - Для некоторых писем нужно вытаскивать данные, для какой-то достаточно ссылки. Предусмотреть проверку на это
    в соответствии со спецификацией по JSON
    """
    with open(cfg.filename, "a") as file: file.write("\nGetting clear date from links...")
    for i in letters:
        i.Body = "Needly dates"
    sleep(1)
    with open(cfg.filename, "a") as file: file.write("Dates gets!")


def FormJSONDates(letters):
    """
    Функционал:
    - Сформировать список, хранящий экземпляры json с данными, необходимыми для отправки по каждой лабораторной
    На входе:
    - convertedLetter - список писем - экземпляров класса Letter, в каждом из которых в поле Body лежит необходимая для
    отправки информация
    На выходе:
    - jsonDates - список json с нужными данными и в нужном формате
    Что предусмотреть:
    - Формат json для каждой лабораторки прописан в спецификации по json, но по факту он везде одинаковый
    - Продумать момент обработки списка писем
    """
    with open(cfg.filename, "a") as file: file.write("\nForming jsons...")
    jsons = []
    for i in range(len(letters)):
        jsons.append("my_json" + str(i))
    sleep(1)
    with open(cfg.filename, "a") as file: file.write("Jsons forms!")
    return jsons

def SendJSONForCheck(jsonDates, letters):
    """
    Функционал:
    - Отправить письма на проверку в модули проверки писем от ВТ
    - Дождаться проверки каждого из писем
    - Сформировать список экземпляров классов LetterResults по каждому письму, расставить оценки и комментарии от ВТ
    На входе:
    - jsonDates - список с экземплярами json, с нужными данными в нужном формате
    - letters - список писем, передаваемый от модуля к модулю. Используются при заполнении экземпляров класса LetterResult
    На выходе:
    - letterResult - заполненный список экземпляров класса LetterResult с результатами обработки писем
    Что предусмотреть:
    - Будет синхронный режим работы, когда сначала отправляется первый json потом происходит ожидание ответа на него,
    после чего происходит заполнение нужных полей
    отправить json1 ->
    получить ответ на json1 ->
    Заполнить нужные поля в result1 ->
    отправить json3 ->
    получить ответ на json3 ->
    Заполнить нужные поля в result3 ->
    отправить json3 ->
    получить ответ на json3 ->
    Заполнить нужные поля в result3 ->
    ...
    - Каждый json нужно отправить на нужный порт. Предусмотреть проверку на это в соответствии со спецификацией по JSON
    - Предусмотеть таймаут ожидания, чтобы система не зависала на бесконечное время при ошибках в модулях проверки
    В этом случае заполнять не только поле IsOK но и поле Code
    """
    with open(cfg.filename, "a") as file: file.write("\nSending jsons...")
    for i in range(len(jsonDates)):
        with open(cfg.filename, "a") as file: file.write("\nSend json " + str(i))
    with open(cfg.filename, "a") as file: file.write("\nJsons sends!")

    with open(cfg.filename, "a") as file: file.write("\nForming letter results...")
    new_letters = []
    for i in letters:
        user = i.Student
        letter = LetterResult(user)
        letter.IsOK = True
        new_letters.append(letter)

    sleep(1)
    with open(cfg.filename, "a") as file: file.write("Letter results forms!")
    return new_letters



