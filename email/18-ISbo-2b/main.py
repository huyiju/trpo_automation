#!/usr/bin/python3
# coding=utf-8
from time import sleep
from datetime import datetime
import sys

from google_CheckEmail import CheckEmail
import config as cfg
from global_Timer import Timer
from reserve_Reserve import Reserve

def Main():
    # try:
    #     print(next(cfg.gen_num_for_filename))
    #     print(next(cfg.gen_num_for_filename))
    #     print(next(cfg.gen_num_for_filename))

        cfg.timer = Timer()
        cfg.reserve_dates = Reserve()
        cfg.filename = cfg.path_to_logs + "log_" + datetime.strftime(datetime.now(), "%Y.%m.%d") + "_" + str(next(cfg.gen_num_for_filename)) + ".txt"

        with open(cfg.filename, "a") as file:
            file.write("\nStart working...")

	while True:
	    CheckEmail()

        with open(cfg.filename, "a") as file:
            file.write("End working!")

    # except Exception:
    #     print("nope")
    #     # with open(cfg.filename, "a") as file: file.write("Sorry, but you have an error")
    #     sleep(1)
    #     # with open(cfg.filename, "a") as file: file.write("Restarting...")
    #     sleep(1)
    #     Main()

if __name__ == '__main__':
    Main()
