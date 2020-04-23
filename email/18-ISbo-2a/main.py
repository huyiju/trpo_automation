import APIgoogle
import client
import Validation
import log_method
import config
#Временная заглушка
log_method.logger.debug('Program start')
service = APIgoogle.get_service()
message_info = APIgoogle.get_message(service, APIgoogle.user_id)
email = APIgoogle.search_email(message_info['email_id'])
if email is None : 
    APIgoogle.send_message(service, APIgoogle.user_id, APIgoogle.cleaning_email(message_info['email_id']), APIgoogle.name_surname(message_info['email_id']), 3, None, None)
    log_method.logger.debug('Program finished')
    exit(1)
valid_dict = Validation.validation(message_info['head_of_msg'], message_info['body_of_msg'])
if len(valid_dict["errorDescription"]) > 0 : 
    APIgoogle.send_message(service, APIgoogle.user_id, APIgoogle.cleaning_email(message_info['email_id']), APIgoogle.name_surname(message_info['email_id']), 2, None, valid_dict)
    log_method.logger.debug('Program finished')
    exit(1)  
answer = client.send_a_laboratory_work_for_verification(labNumber = valid_dict['Number'], labLink = valid_dict['URL'])
data_user = APIgoogle.search_group(email)
cell = APIgoogle.search_tablic(data_user[0], valid_dict['Number'], data_user[1]) 
if answer == 0 : 
    APIgoogle.send_message(service, APIgoogle.user_id, APIgoogle.cleaning_email(message_info['email_id']), APIgoogle.name_surname(message_info['email_id']), 1, answer, None)
    APIgoogle.add_mark_in_table(data_user[0], cell, 0)
    log_method.logger.debug('Program finished')
    exit(1)


APIgoogle.add_mark_in_table(data_user[0], cell, 1)
APIgoogle.send_message(service, APIgoogle.user_id, email, APIgoogle.name_surname(message_info['email_id']), 0, None, None)
log_method.logger.debug('Program finished')