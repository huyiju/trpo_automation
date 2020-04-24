# coding=utf-8
import socket
import global_LetterResult
import json
import select

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

    for tmp in letters:
        html = get_html(tmp.Body) 
        tmp.Body = finding_files(html, tmp.Student.NameOfStudent)
    return letters



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
        if letters[i].CodeStatus == "20":
            json1 = {
                "messageType" : 1,
                "lab" : letters[i].NumberOfLab,
                "variant" : letters[i].VariantOfLab,
                "link" : None,
                "code" : letters[i].Body
                }
            mystr = json.dumps(json1)
            jsonDates.append(mystr)

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

    "Список новых писем"
    new_letters = []

    conf = open("config_port.json", "r")
    config = conf.read()
    """Соответствие номера лабораторной и номера порта"""
    dataLab = json.loads(config)
    """Счётчик для параллельного обращения в два списка"""
    count = 0
    for i in letters:
        letter = global_LetterResult.LetterResult()

        """Данные для подключения"""
        sock = socket.socket()
        port = dataLab[str(i.NumberOfLab)]
        config = open("configServ.txt", "r")
        HOST = config.readline()
        HOST = HOST.replace("\n", '')
        if i.CodeStatus == "20":
            continue

        """Подключение и отправка JSON на порт"""
        sock.connect((HOST, port))
        sock.send(jsonDates[count].encode())
        count += 1
        IsOk = False

        """Ожидание ответа сервера 10 секунд"""
        ready = select.select([sock], [], [], 10)
        if ready[0]:
            otv_serv = sock.recv(1024)
            otvetServ = json.loads(otv_serv.decode())
            if otvetServ["messageType"] == 2:
                if otvetServ["grade"] == 1:
                    IsOk = True
                letter.Comment = otvetServ["comment"]
                letter.CodeStatus = "30"
                letter.Comment = ""

            elif otvetServ["messageType"] == 3:
                letter.CodeStatus = "07"
                letter.CodeStatusComment = ""
                letter.Comment = otv_serv.decode()

            elif otvetServ["messageType"] == 4:
                letter.CodeStatus = "06"
                letter.CodeStatusComment = ""
                letter.Comment = otv_serv.decode()
        else:
            sock.close()
            letter.CodeStatus = "06"
            letter.CodeStatusComment = "ERROR. Длительное ожидание ответа от сервера"

        """Заполнение полей letterResult"""
        letter.Student = i.Student
        letter.ThemeOfLetter = i.ThemeOfLetter
        letter.IsOK = IsOk
        letter.VariantOfLab = i.VariantOfLab
        letter.NumberOfLab = i.NumberOfLab

        """Добавление нового письма"""
        new_letters.append(letter)
        sock.close()

    return new_letters



