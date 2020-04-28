# coding=utf-8
from time import sleep
from datetime import datetime

from moderate_FormAnswers import FormAnswers
import config as cfg

def SetResults(letterResults):
    """
    Выставить необходимые оценки в журнал
    """

    SetMarks(letterResults)

    FormAnswers(letterResults)

def SetMarks(letterResults):
    """
     Функционал:
    - Выставить необходимые оценки в журнал
    На входе:
    - letterResults - заполненный и проверенный список писем - экземпляров класса LetterResults
    На выходе:
    - None
    Что предусмотреть:
    - None
    """
    with open(cfg.filename, "a") as file: file.write("\nSetting marks...")
    sleep(1)
    with open(cfg.filename, "a") as file: file.write("End settings!")
