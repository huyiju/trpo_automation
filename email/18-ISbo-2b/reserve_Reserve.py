# coding=utf-8
from time import sleep
from datetime import datetime

import config as cfg

class Reserve:

    ReservePeoples = ""
    ReserveMarks = ""

    def __init__(self):
        pass

    def GetReserveDate(self):
        """
        Функционал:
        - Получить резервные данные для восстановления
        В зависимости от выбранного подхода это:
        - - Либо данные по двум журналам - доступа и оценок
        - - Либо номера версий журналов
        На входе:
        - None
        На выходе:
        - Копии журналов / номера версий журналов (глобальные переменные)
        Что предусмотреть:
        - None
        Участвующие внешние типы переменных
        - global version_assess / journal_assess
        - global version_marks / journal_marks
        """
        with open(cfg.filename, "a") as file: file.write("\nGetting reserve dates...")
        ReservePeoples = "Value1"
        ReserveMarks = "Value2"
        sleep(1)
        with open(cfg.filename, "a") as file: file.write("Reserve date gets!")