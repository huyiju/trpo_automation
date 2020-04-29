# coding=utf-8
from datetime import datetime

timer = None
reserve_dates = None
filename = ""
timeout = 10


def num_for_filename():
    n = 1
    while True:
        yield n
        n += 1

gen_num_for_filename = num_for_filename()
last_date = datetime.strftime(datetime.now(), "%Y.%m.%d")
path_to_logs = "/home/rurec/git/temp/trpo_automation/email/18-ISbo-2b/logs/"
