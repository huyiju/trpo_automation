# coding=utf-8
from time import sleep
from datetime import datetime

import PatternsofLetter
from global_AnswersForUsers import AnswersForUsers
from send_InformUsers import InformUsers
import config as cfg


def FormAnswers(letterResult):
    """
    Формирование ответов пользователям
    """

    answers = MakeAnswersForUsers(letterResult)

    InformUsers(answers)


def MakeAnswersForUsers(letterResult):
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
    techer = False
    forteacher = PatternsofLetter.ForTeacher
    for i in letterResult:
        if letterResult[i].CodeStatus == "00":
            pattern = PatternsofLetter.UnknownUser
        elif letterResult[i].CodeStatus == "01":
            pattern = PatternsofLetter.UncorrectedTheme
        elif letterResult[i].CodeStatus == "02":
            pattern = PatternsofLetter.UncorrectedStructure
        elif letterResult[i].CodeStatus == "03":
            pattern = PatternsofLetter.UncorrectedVariant
        elif letterResult[i].CodeStatus == "04":
            pattern = PatternsofLetter.LostLinks
        elif letterResult[i].CodeStatus == "05":
            pattern = PatternsofLetter.HaveAttachments
        elif letterResult[i].CodeStatus == "06":
            pattern = PatternsofLetter.SystemFailure
        elif letterResult[i].CodeStatus == "07":
            pattern = PatternsofLetter.SystemFailure
        elif letterResult[i].CodeStatus == "10":
            pattern = PatternsofLetter.WorkCompleted
        elif letterResult[i].CodeStatus == "30":
            pattern = PatternsofLetter.WorkVerified(letterResult[i].IsOk)
            par = (letterResult[i].Student.NameOfStudent, letterResult[i].NumberOfLab, letterResult[i].VariantOfLab)
            forteacher.add(par)
            techer = True
        answer = AnwersForUsers(letterResult[i].Student.email, pattern.return_theme(), answers[i])
        answers.append(answer)
    sleep(1)
    if techer == True
    answer = AnswersForUsers(cfg.teacher_email, forteacher.return_theme(), forteacher.return_body())
    answers.append(answer)
    with open(cfg.filename, "a") as file: file.write("Answers for users forms!")
    return answers
