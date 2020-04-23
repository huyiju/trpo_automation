import log_method


@log_method.log_method_info
def validation(head_of_msg,body_of_msg):
    
    Subjects_list = ['ТРПО'] # Список предметов
    SubjectNumber_list = ['ЛР№1', 'Лабораторная работа №1', 
                          'ЛР№2', 'Лабораторная работа №2',
                          'ЛР№3', 'Лабораторная работа №3',
                          'ЛР№4', 'Лабораторная работа №4',
                          'ЛР№5', 'Лабораторная работа №5',
                          'ЛР№6', 'Лабораторная работа №6',
                          'ЛР№7', 'Лабораторная работа №7',
                          'ЛР№8', 'Лабораторная работа №8',
                          'ЛР№9', 'Лабораторная работа №9']
    Errors_list = [] # Список ошибок
    Greeting_list = ['Добрый день','Добрый вечер'] # Список приветствий
    for x in Subjects_list: # Проверка на название предмета
        a = head_of_msg.find(x)
        if a != -1:
            break
    if a == -1:
        log_method.logger.warning('validation: The name of \
                                   item is incorrect.')
        Errors_list.append('неверно указано название предмета')
    for x in SubjectNumber_list: # Проверка на номер лабораторной
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
    for x in Greeting_list: # Проверка на приветствие 
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
            # Ищем первый пробел после http
            while  a + counter < len(body_of_msg)-1:
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

    

