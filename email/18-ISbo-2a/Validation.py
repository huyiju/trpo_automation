import log_method
from pattern import *


@log_method.log_method_info
def validation(head_of_msg,body_of_msg):
    Errors_list = [] # Список ошибок
    for x in SUBJECT_LIST: # Проверка на название предмета
        a = head_of_msg.find(x)
        if a != -1:
            break
    if a == -1:
        log_method.logger.warning('validation: The name of \
                                   item is incorrect.')
        Errors_list.append('неверно указано название предмета')
    for x in SUBJECTNUMBER_LIST: # Проверка на номер лабораторной
        a = head_of_msg.find(x)
        if a != -1:
            a = head_of_msg.find('№')
            Number=head_of_msg[a+1]
            break
    if a == -1:
        log_method.logger.warning('validation: The lab number \
                                   is incorrect.')
        Errors_list.append('неверно указан номер ЛР')
        Number = None
    for x in GREATING_LIST: # Проверка на приветствие 
        a = body_of_msg.find(x)
        if a != -1:
            break
    if a == -1:
        log_method.logger.warning('validation: Missing greeting.')
        Errors_list.append('отсутствует приветствие')
    URL=url_cheack(Number,body_of_msg) # Проверка на URL
    a = body_of_msg.find('--') # Проверка на подпись
    if a == -1:
        log_method.logger.warning('validation: Missing signature.')
        Errors_list.append('отсутствует подпись')
    validation_dictionary={ # Словарь
     'Number':Number,
     'URL': URL,
     "errorDescription": Errors_list
    }
    return(validation_dictionary)
    
@log_method.log_method_info
def url_cheack(Number,body_of_msg): # Проверка на наличие URL. Возврат ссылки.
    SubjectNumberURL_list = ['7', '8', '9'] # Список ЛР c URL
    for x in SubjectNumberURL_list:  # Проверка на содержание URL
        if Number == x:
            a = body_of_msg.find('http')
            counter = 0
            while  a + counter < len(body_of_msg)-1:# Ищем пробел после http
                if body_of_msg[a + counter] != ' ':
                    counter = counter + 1
                else:
                    break        
            if a+counter == len(body_of_msg)-1: # Дошли не найдя пробелов
                if body_of_msg[a + counter] == '.':
                    URL = body_of_msg[a:a + counter]
                    return(URL)
                else:
                    URL=body_of_msg[a:a + counter + 1]
                    return(URL) 
            while a + counter >= a:
                if body_of_msg[a + counter] == '.':
                    URL = body_of_msg[a:a + counter]
                    logging.debug('url = %s' % URL)
                    return (URL)                  
                if body_of_msg[a + counter] != '.':
                    counter = counter - 1  