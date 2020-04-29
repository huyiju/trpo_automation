# coding=utf-8
from time import sleep
from datetime import datetime

import config_Project as cfg

class Timer:

    timer = None

    def __init__(self):
        pass

    def SetTimer(self):
        """
        Функционал:
        - Поставить таймер на необходимое время,
        На входе:
        - None
        На выходе:
        - None
        Что предусмотреть:
        - None
        Участвующие внешние типы переменных
        - None
        """
        with open(cfg.filename, "a") as file: file.write("\nSetting timer...")

        timer = 10
        with open(cfg.filename, "a") as file: file.write("Timer sets!")


    def WaitForTimer(self):
        """
        Функционал:
        - Дождаться таймера
        На входе:
        - None
        На выходе:
        - None
        Что предусмотреть:
        - None
        Участвующие внешние типы переменных
        - None
        """
        with open(cfg.filename, "a") as file: file.write("\nWaiting for timer...")

        timer = 0
        with open(cfg.filename, "a") as file: file.write("Timer ends!")

