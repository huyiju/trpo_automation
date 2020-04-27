# coding=utf-8
from time import sleep
from datetime import datetime

from global_AnswersForUsers import AnswersForUsers
from send_InformUsers import InformUsers
import config as cfg
import PatternofLetter

def FormAnswers(letterResult):
    """
    Формирование ответов пользователям
    """

    answers = MakeAnswers(letterResult)

    answers = MakeAnswersForUsers(answers, letterResult)

    InformUsers(answers)

def MakeAnswers(letterResult):
    """
    Функционал:
    - Сделать список хранящий в себе ответы на каждое письма
    На входе:
    - Список проверенных писем - экземпляяров класса LetterResults
    На выходе:
    - answers - список ответов на письма в текстовом формате
    Что предусмотреть:
    - Создание класса, в котором будут размещены уже готовые ответы на письма
    - Заполнение всех полей, в зависимости от характеристик письма:
    - - Оценки
    - - Имени, фамилии ученика
    - - Статуса письма
    - В конце формирование письма для преподавателя на основе всех писем. В письме указать
    - - Кто и какую оценку получил
    Участвующие внешние типы переменных
    - Класс с экземплярами написанныш шаблонов писем - из import
    """
    with open(cfg.filename, "a") as file: file.write("\nForming answers...")
    answers = []
    for i in letterResult:
        if letterResult[i].CodeStatus == 0:
            pattern = PatternofLetter.UnknownUser
        elif letterResult[i].CodeStatus == 1:
            pattern = PatternofLetter.UncorrectTheme
        elif letterResult[i].CodeStatus == 2:
            pattern = PatternofLetter.UncorrectStructure
        elif letterResult[i].CodeStatus == 3:
            pattern = PatternofLetter.UncorrectVariant
        elif letterResult[i].CodeStatus == 4:
            pattern = PatternofLetter.LostLinks
        elif letterResult[i].CodeStatus == 5:
            pattern = PatternofLetter.HaveAttachments
        elif letterResult[i].CodeStatus == 6:
            pattern = PatternofLetter.SystemFailure
        elif letterResult[i].CodeStatus == 7:
            pattern = PatternofLetter.SystemFailure
        elif letterResult[i].CodeStatus == 10:
            pattern = PatternofLetter.WorkComplited
        elif letterResult[i].CodeStatus == 30:
            pattern = PatternofLetter.WorkVerified
        answers.append(pattern.returnbody())
    sleep(1)
    with open(cfg.filename, "a") as file: file.write("Answers forms!")


def MakeAnswersForUsers(answers, letterResult):
    """
    Функционал:
    - Сформировать список экземпляров класса AnswersForUsers, используя уже готовые ответы на письма
    На входе:
    - Список проверенных писем - экземпляров класса LetterResults и сформированные ответы на письма
    На выходе:
    - answers - список экземпляров класса AnswersForUsers, в котором находятся все необходимые для отправки письма
    Что предусмотреть:
    - поле Who заполняется из письма из поля Student из поля Email
    - поле What заполняется из текстового ответа на это письмо
    - для преподавателя нет письма, из которого можно достать Email, поэтому это нужно вписать в программу вручную
    Участвующие внешние типы переменных
    - AnswersForUsers - из import
    """
    with open(cfg.filename, "a") as file: file.write("\nForming answers for users...")
    answers = []
    for i in letterResult:
        if letterResult[i].CodeStatus == 0:
            pattern = PatternofLetter.UnknownUser
        elif letterResult[i].CodeStatus == 1:
            pattern = PatternofLetter.UncorrectTheme
        elif letterResult[i].CodeStatus == 2:
            pattern = PatternofLetter.UncorrectStructure
        elif letterResult[i].CodeStatus == 3:
            pattern = PatternofLetter.UncorrectVariant
        elif letterResult[i].CodeStatus == 4:
            pattern = PatternofLetter.LostLinks
        elif letterResult[i].CodeStatus == 5:
            pattern = PatternofLetter.HaveAttachments
        elif letterResult[i].CodeStatus == 6:
            pattern = PatternofLetter.SystemFailure
        elif letterResult[i].CodeStatus == 7:
            pattern = PatternofLetter.SystemFailure
        elif letterResult[i].CodeStatus == 10:
            pattern = PatternofLetter.WorkComplited
        elif letterResult[i].CodeStatus == 30:
            pattern = PatternofLetter.WorkVerified
        answer = AnwersForUsers(letterResult[i].Student.email, pattern.returntheme(), answers[i])
        answers.append(answer)
    sleep(1)
    with open(cfg.filename, "a") as file: file.write("Answers for users forms!")
    return answers
