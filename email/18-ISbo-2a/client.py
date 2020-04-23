import socket
import json
from config import PORTS
import log_method
import random

##def SendURL(url, student, studentgroup, labnumber, port):
@log_method.log_method_info
def send_a_laboratory_work_for_verification(**kwargs): 
    """
    Метод, отправляющий работу на проверку
    **kwargs - все параметры Лабораторной работы
    """
    '''
    data = ({
        "labNumber": str(kwargs['labNumber']),
        "labLink": str(kwargs['labLink']),
    }) #Создание JSON
    jsn = json.dumps(data)
    sock = socket.socket() #Создание сокета
    sock.connect(("127.0.0.1",int(PORTS[str(kwargs['labNumber'])]))) #Подключение
    log_method.logger.debug('send_a_laboratory_work_for_verification: Connect to 127.0.0.1:%s' % PORTS[str(kwargs['labNumber'])])
    sock.send(jsn) #Отправка
    log_method.logger.debug('send_a_laboratory_work_for_verification: Send file')
    response = sock.recv(1024) #Получение ответа
    log_method.logger.debug('send_a_laboratory_work_for_verification: Accepted the responce')
    '''
    response = {
        "labStatus": random.randint(0,1)
    }
    while response:
        if (response["labStatus"]==1):
            #sock.close()
            return 1
        elif (response["labStatus"]==0):
            #sock.close()
            return 0
        #response = sock.recv(1024)

    #sock.close()
    return 0
