import APIgoogle
import client
import Validation
import log_method
import config
import time

while True:
    log_method.logger.debug('Program start')
    #Получение открытого сервиса для работы с API.
    service = APIgoogle.get_service()
    #Получение информации о последнем письме.
    message_info = APIgoogle.get_message(service, APIgoogle.user_id)

    if message_info:
        #Проверка сценария на нахождения email в таблице
        email = APIgoogle.search_email(message_info['email_id'])
        if email is None : 
            APIgoogle.send_message(service, APIgoogle.user_id, 
                                APIgoogle.cleaning_email(message_info['email_id']), 
                                APIgoogle.name_surname(message_info['email_id']), 
                                3, None, None)
        else:
            #Проверка валидации письма
            valid_dict = Validation.validation(message_info['head_of_msg'], message_info['body_of_msg'])
            if len(valid_dict["errorDescription"]) > 0 : 
                APIgoogle.send_message(service, APIgoogle.user_id, 
                                    APIgoogle.cleaning_email(message_info['email_id']), 
                                    APIgoogle.name_surname(message_info['email_id']), 
                                    2, None, valid_dict)
            else:
                #Получение результата из модуля проверки
                answer = client.send_a_laboratory_work_for_verification(labNumber = valid_dict['Number'], labLink = valid_dict['URL'])
                
                #Получение группы пользователя
                data_user = APIgoogle.search_group(email)
                #Получение ячейка в журнале
                cell = APIgoogle.search_tablic(data_user[0], valid_dict['Number'], data_user[1]) 
                
                #Лабораторная неправильно сделана
                if answer == 0: 
                    APIgoogle.send_message(service, APIgoogle.user_id, 
                                        APIgoogle.cleaning_email(message_info['email_id']), 
                                        APIgoogle.name_surname(message_info['email_id']), 
                                        1, answer, None)
                    APIgoogle.add_mark_in_table(data_user[0], cell, 0)
                else:
                    #Лабораторная сделана правильно
                    APIgoogle.add_mark_in_table(data_user[0], cell, 1)
                    APIgoogle.send_message(service, APIgoogle.user_id, email, 
                                        APIgoogle.name_surname(message_info['email_id']), 
                                        0, None, None)
        APIgoogle.email_archiving(service, APIgoogle.user_id, message_info)
    else:
        time.sleep(1000)

    log_method.logger.debug('Program finished')