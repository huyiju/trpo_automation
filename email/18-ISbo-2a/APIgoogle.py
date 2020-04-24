#coding: utf-8
import pickle
import os.path
import httplib2
import apiclient.discovery
import re;
import email
import base64
import log_method
from oauth2client.service_account import ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from datetime import datetime
from pprint import pprint
from config import SPREAD_SHEET_ID
from config import CREDENTIALS_FILE
from config import SPREAD_SHEET_ID_INIT
from config import CREDENTIALS_FILE_SERVICE
from pattern import *



SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.labels',
          'https://www.googleapis.com/auth/gmail.modify']


@log_method.log_method_info
def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            	CREDENTIALS_FILE_SERVICE,
                SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


service = get_service()
user_id = 'me'

@log_method.log_method_info
def add_mark_in_table(table, cell, mark):
    log_method.logger.debug(f'add_mark_in_table: table - {table}, \
							  cell - {cell}, mark - {mark}')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
				  CREDENTIALS_FILE, 
				  ['https://www.googleapis.com/auth/spreadsheets',
				  'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) 
    rangeTab = "(ТРПО) " + str(table) + "!" + str(cell)
    service.spreadsheets().values().batchUpdate(spreadsheetId =
		SPREAD_SHEET_ID, body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": rangeTab,
                "majorDimension": "ROWS",     
                "values": [ [mark] ]
            }
        ]
    }).execute()

        
@log_method.log_method_info
def cleaning_email(email_id):
    """
    Метод для выделения почты из передаваемой строки email.
    email - передаваемая строка с почтой
    Name Surname <1234@gmail.com> ← пример email который мне передают
    1234@gmail.com это будет запоминаться после метода очистки
    """
    comp = re.compile(r'<(\S*?)>')
    y = comp.search(email_id)
    q = y.group(0)
    z = q.replace('<', '').replace('>', '')
    return z


@log_method.log_method_info
def name_surname(email_id):
    """ Метод для выделения и передачи имени и фамилии."""
    comp = re.compile('(\S*?) '+'(\S*?) ')
    y = comp.search(email_id)
    return y.group(0)


@log_method.log_method_info
def search_email(email_id):
    """Метод для поиска в таблице."""
    mail_str = cleaning_email(email_id)
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
                CREDENTIALS_FILE,
                ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    range_name = 'List1!B1:B1000'
    table = service.spreadsheets().values().get(
          spreadsheetId=SPREAD_SHEET_ID,
          range=range_name).execute()
    if re.search(mail_str, str(table)):
        return mail_str
    else:
        return None


@log_method.log_method_info
def get_message(service, user_id):
    """ 
    Метод получения полезной информации из письма студента.
    """
    search_id = service.users().messages().list(userId=user_id,
                                                labelIds = ['INBOX']).execute()
    message_id = search_id['messages']
    alone_msg = message_id[0]
    id_of_msg = alone_msg['id']
    message_list = service.users().messages().get(userId=user_id, 
                                                  id=id_of_msg,
                                                  format='full').execute()
    info_of_msg = message_list.get('payload')['headers']
    email_id = ''
    head_of_msg = ''
    body_of_msg = ''
    for head in info_of_msg :
        if head['name'] == 'From' :
            email_id = head['value']
        if head['name'] == 'Subject' :
            head_of_msg = head['value']
    body_of_msg = message_list['snippet']

    message_info = {'id_of_msg':id_of_msg,
                    'email_id':email_id,
                    'head_of_msg':head_of_msg,
                    'body_of_msg':body_of_msg}
    return message_info


@log_method.log_method_info
def email_archiving(service, user_id, message_info):
     """
    Архивация сообщения.
    
    service: авторизация через мыло.  
    user_id: наше мыло или спец слово 'me'.  
    message_info: словарь с данными письма.
    """
    msg_labels = {'removeLabelIds': ['UNREAD', 'INBOX'],
                  'addLabelIds': ['Label_4436622035204509097']}
    message = service.users().messages().modify(userId=user_id,
                                                id=message_info['id_of_msg'],
                                                body=msg_labels).execute()


@log_method.log_method_info
def send_message(service, user_id, email_of_student, name_of_student,
                 number_of_templates, validation_dictionary, error_dictionary):
    """
    Метод по отправке сообщения студенту.  
    
    service: авторизация через мыло.  
    user_id: наше мыло или спец слово 'me'.  
    email_of_student: мыло студента.  
    name_of_student: имя и фамилия студента.  
    validation_dictionary: словарь с валидации письма, 
    в котором есть ('Numder')номер работы и ('URL')ссылка на работу.  
    error_dictionary: словарь с ошибками в коде студента.  
    number_of_templates: номер используемого для заполнения письма шаблона. 
    """

    str_of_val_er = ""
    str_of_er = "" 
    if number_of_templates == 1:
        str_of_val_er = error_in_work(validation_dictionary)
    else:
        if number_of_templates == 2:
            str_of_er = error_in_work(error_dictionary)
        else:
            str_of_val_er = ""
            str_of_er = ""    

    message_templates = funcSt(str_of_val_er, str_of_er)

    sending_msg = {}
    hello_student = funcHello(name_of_student)
    sending_msg['from'] = GMAIL_OF_TRPO
    our_msg = message_templates[number_of_templates]['our_msg']
    title = message_templates[number_of_templates]['title']

    sending_msg = MIMEMultipart('alternative')
    sending_msg = MIMEText(hello_student + our_msg + SIGNATURE)
    sending_msg['To'] = email_of_student
    sending_msg['Subject'] = title

    raw = base64.urlsafe_b64encode(sending_msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}

    send_msg = service.users().messages().send(userId=user_id, 
                                               body=body).execute()
    

@log_method.log_method_info
def send_message_to_techsub(service, user_id, email_of_student, 
                            name_of_student, validation_dictionary, 
                            error_dictionary, number_of_templates):
    """
    Рассылка писем ТП.
    Вызывается преподавателю, если у студента есть ошибки в работе
    или ТП, если упал один из модулей
    service: авторизация через мыло
    user_id: наше мыло или спец слово 'me'
    email_of_student: мыло студента
    name_of_student: имя и фамилия студента
    validation_dictionary: словарь с валидации письма, 
    в котором есть ('Numder')номер работы и ('URL')ссылка на работу
    error_dictionary: словарь с ошибками в коде студента
    number_of_templates: номер используемого для заполнения письма шаблона
    """

    if number_of_templates == 0:
        str_of_er = error_in_work(error_dictionary)
    else:
        str_of_er = ""

    message_templates = funcTs(name_of_student, validation_dictionary, 
                                       str_of_er)
    sending_msg = {}

    sending_msg['From'] = GMAIL_OF_TRPO

    sending_msg = MIMEMultipart('alternative')
    sending_msg = MIMEText(message_templates[number_of_templates]['hello'] + 
                           message_templates[number_of_templates]['our_msg'] + 
                           SIGNATURE)
    sending_msg['Subject'] = message_templates[number_of_templates]['title']
    if number_of_templates != 0:
        for i in MAS_OF_TO:
            sending_msg['To'] = i

            raw = base64.urlsafe_b64encode(sending_msg.as_bytes())
            raw = raw.decode()
            body = {'raw': raw}
    else:
        sending_msg['To'] = EMAIL_OF_TEACHER

        raw = base64.urlsafe_b64encode(sending_msg.as_bytes())
        raw = raw.decode()
        body = {'raw': raw}

    send_msg = service.users().messages().send(userId=user_id,
                                               body=body).execute()
    

@log_method.log_method_info
def error_in_work(some_errors):
    """
    Метод преобразования массива с ошибками в строку
    Метод используется для валидации и ошибок кода студента
    """
    error = ""
    mas_of_er = some_errors["errorDescription"]
    i = 0
    while i < len(mas_of_er):
        error += "- " + mas_of_er[i] + "\n"
        i += 1
    return error


@log_method.log_method_info
def search_group(email_id):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
                CREDENTIALS_FILE,
                ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    spreadsheetId = SPREAD_SHEET_ID_INIT
    range_name = 'List1!B1:B1000'
    table = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId,
            range=range_name).execute()
    c = 1
    for val in table.get('values'):
        if val[0] != email_id:
            c += 1
        else:
            break
    if c == len(table.get('values'))+1:
        return None
    else:
        nomer = f'List1!F{c}:G{c}'
        table1 = service.spreadsheets().values().get(
               spreadsheetId=spreadsheetId, range=nomer).execute()
        values_finish = table1.get('values')[0]
        return tuple(values_finish)


@log_method.log_method_info
def search_tablic(group, laba, surname):
    group1 = '(ТРПО) '+group
    c = 2
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
                CREDENTIALS_FILE,
                ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    spreadsheetId = SPREAD_SHEET_ID
    range_name = group1+'!D2:D1000'
    table = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=range_name).execute()
    count = ord('J') + int(laba)-1
    nomer_stolbca = chr(count)
    try:
        for name in table.get('values'):
            if name[0] != surname:
                c = c+1
            else:
                break
        position = str(chr(count)) + str(c)
    except:
        return None
    else:
        return position
