import APIgoogle
import client
import Validation
import log_method
import config
import time

log_method.logger.debug('main: Program start')
while True:
    #Получение открытого сервиса для работы с API.
    service = APIgoogle.get_service()
    #Получение информации о последнем письме.
    message_info = APIgoogle.get_message(service, APIgoogle.user_id)

    if message_info:
        log_method.logger.debug('main: A new letter was found')
        #Проверка сценария на нахождения email в таблице
        email = APIgoogle.search_email(message_info['email_id'])
        if email is None : 
            log_method.logger.warning('main: No mail was found in the table - %s' % message_info['email_id'])
            APIgoogle.send_message(service, APIgoogle.user_id, 
                                APIgoogle.cleaning_email(message_info['email_id']), 
                                APIgoogle.name_surname(message_info['email_id']), 
                                3, None, None)
        else:
            #Проверка валидации письма
            valid_dict = Validation.validation(message_info['head_of_msg'], message_info['body_of_msg'])
            if len(valid_dict["errorDescription"]) > 0 : 
                log_method.logger.warning('main: The letter did not pass validation from %s' % message_info['email_id'])
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
                    log_method.logger.warning('main: Lab done wrong from %s' % message_info['email_id'])
                    APIgoogle.send_message(service, APIgoogle.user_id, 
                                        APIgoogle.cleaning_email(message_info['email_id']), 
                                        APIgoogle.name_surname(message_info['email_id']), 
                                        1, answer, None)
                    APIgoogle.add_mark_in_table(data_user[0], cell, 0)
                else:
                    #Лабораторная сделана правильно
                    log_method.logger.info('main: Lab done right from %s' % message_info['email_id'])
                    APIgoogle.add_mark_in_table(data_user[0], cell, 1)
                    APIgoogle.send_message(service, APIgoogle.user_id, email, 
                                        APIgoogle.name_surname(message_info['email_id']), 
                                        0, None, None)
        APIgoogle.email_archiving(service, APIgoogle.user_id, message_info)
    else:
        log_method.logger.debug('main: No new letters found...')
        time.sleep(1000)

log_method.logger.debug('main: Program finished')