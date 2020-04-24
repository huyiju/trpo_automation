import inspect
import datetime
class Logs:

    toInput = None
    defName = None

    def __init__(self):
        pass

    def Create(self, input_info, def_name):
        self.toInput = input_info
        self.defName = def_name

    def FormErrorLog(self):
        time = datetime.datetime.now()
        status = "ERROR"
        def_name = self.defName
        input_value = self.toInput

        print(time, status, "функция", def_name, "входной параметр", input_value)

    def FormCommonLog(self):
        time = datetime.datetime.now()
        status = "OK"
        def_name = self.defName
        input_value = self.toInput

        print(time, status, "функция", def_name, "входной параметр", input_value)
