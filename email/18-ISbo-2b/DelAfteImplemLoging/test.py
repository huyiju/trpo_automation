import inspect
import logging
logging.basicConfig(filename="log2.txt", level = logging.DEBUG)
from logs import Logs

# объявляешь в глобальных переменных
logs = Logs()

def myfunc(a):
    logging.info("Вызвана функция  %s с параметрами %s" % (inspect.currentframe().f_code.co_name,a))
    # место где ты получаешь данные о функции

    print("Получение данных...")

    # после этого заполняешь поля
    toInput = a
    defName = inspect.currentframe().f_code.co_name

    logs.Create(toInput, defName)

    # ------------------------------------------- #
    print(3/a)
    return 4
    # ------------------------------------------- #

try:
    logging.basicConfig(filename="mySnake.log", level=logging.INFO)
    logging.info("Program started")
    myfunc(0)


    logs.FormCommonLog()
except Exception as e:
    logging.error(str(e))
    logs.FormErrorLog()

finally:
    logging.info("Program end")
        
        


