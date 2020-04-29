#!/usr/bin/python3
# coding=utf-8
from time import sleep
from datetime import datetime
from threading import Timer

from main_1_google_CheckEmail import CheckEmail
import config_Project as cfg
from reserve_Reserve import Reserve


def Main():
    # try:
        # Создание объекта резервных данных
        cfg.reserve_dates = Reserve()

        # Формирование имени файла лога
        cfg.filename = cfg.path_to_logs + "log_" + datetime.strftime(datetime.now(), "%Y.%m.%d") + "_" + str(next(cfg.gen_num_for_filename)) + ".txt"

        # Запись в лог о начале работы
        with open(cfg.filename, "a") as file:
            file.write("Начало работы... ")

        # Запуск работы
        # while True:
            # Установка таймаута ожидания
        start_function = Timer(cfg.timeout, CheckEmail)

        # Запуск таймера до начала работы
        start_function.start()

    # except Exception as err:
    #
    #     # Запись в лог о ошибке
    #     with open(cfg.filename, "a") as file:
    #         file.write("Извините, у вас возникла ошибка, " + str(err) + " перезапускаю...")
    #
    #     # Перезапуск
    #     Main()

# Вызов начальной функции
if __name__ == '__main__':
    Main()
