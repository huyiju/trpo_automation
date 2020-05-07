import unittest
import httplib2
import requests
import crypto
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

class Test_google(unittest.TestCase):
    
    def setUp(self):
        crypto.decrypt_file('Example.json.bin')
        crypto.decrypt_file('config.py.bin')
        crypto.decrypt_file('token.pickle.bin')

    def tearDown(self):
        crypto.crypt_file('Example.json')
        crypto.crypt_file('config.py')
        crypto.crypt_file('token.pickle')

    def test_add_mark(self):
        from config import SPREAD_SHEET_ID
        from config import CREDENTIALS_FILE
        from APIgoogle import add_mark_in_table
        add_mark_in_table('(ТРПО) 18-ИСбо-2а', 'M8', '2')
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

        ranges = '(ТРПО) 18-ИСбо-2а!M8'
        request = service.spreadsheets().values().get(spreadsheetId = SPREAD_SHEET_ID, range = ranges)
        response = request.execute();
        new_one = response['values'][0][0]
        self.assertEqual(new_one, '2')

    def test_search_group(self):
        from config import SPREAD_SHEET_ID_INIT
        from config import CREDENTIALS_FILE
        from APIgoogle import search_group

        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',  'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
        spreadsheetId = SPREAD_SHEET_ID_INIT
        test_number = 57

        place_of_our_testing_email=f'List1!B{test_number}'
        table = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=place_of_our_testing_email).execute()
        our_email = table.get('values')[0][0]

        set_group = search_group(our_email)

        nomer=f'List1!F{test_number}:G{test_number}'
        table1 = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=nomer).execute()
        values_finish=table1.get('values')[0]
        values_for_test = tuple(values_finish)
        self.assertEqual(set_group, values_for_test)

    def test_cleaning_email(self):

        from APIgoogle import cleaning_email

        email = cleaning_email('VOLODYA KOTLYAROV <httprequests.is.good@gmail.com>')
        self.assertEqual(email, 'httprequests.is.good@gmail.com')

    def test_name_surname(self):

        from APIgoogle import name_surname

        not_a_email = name_surname('VOLODYA KOTLYAROV <httprequests.is.good@gmail.com>')
        self.assertEqual(not_a_email, 'VOLODYA KOTLYAROV ')

    # def test_search_email(self):

        # from APIgoogle import search_email

    def test_get_service(self):
        from config import SPREAD_SHEET_ID
        from config import CREDENTIALS_FILE
        from APIgoogle import get_service       
        service = get_service();

        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

        service.spreadsheets().values().batchUpdate(spreadsheetId = SPREAD_SHEET_ID, body = {
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": '(ТРПО) 18-ИСбо-2а!P8',
                 "majorDimension": "ROWS",     
                 "values": [ ['4'] ]
                }
            ]
        }).execute()

        request = service.spreadsheets().values().get(spreadsheetId = SPREAD_SHEET_ID, range = '(ТРПО) 18-ИСбо-2а!P8')
        response = request.execute();
        new_one = response['values'][0][0]
        self.assertEqual(new_one, '4')

    def test_get_message(self):
        
        from APIgoogle import get_message
        from APIgoogle import get_service

        service = get_service()
        user_id = 'sanyabl.atchtozah.inya@gmail.com'
        message_info = get_message(service, user_id)
        
        search_id = service.users().messages().list(userId=user_id, labelIds = ['INBOX']).execute()
        message_id = search_id['messages']
        alone_msg = message_id[0]
        id_of_msg = alone_msg['id']
        hello_student = "Здравствуйте, " + 'человек, который делает всё невовремя' + "!"
        signature = " С уважением, Бот"
        our_msg = ' В Вашей работе обнаружены ошибки: ' + '- неверно указан номер ЛР ' + 'Просьба исправить их и отправить письмо повторно.'
        body_of_msg = hello_student + our_msg + signature

        our_info = {
            'id_of_msg':id_of_msg,
            'email_id':user_id,
            'head_of_msg':'Обнаружены ошибки в работе',
            'body_of_msg':body_of_msg
            }

        self.assertEqual(message_info, our_info)

    def test_error_in_word(self):

        from APIgoogle import error_in_work

        Errors_list=[]
        Errors_list.append('неверно указано название предмета')
        Errors_list.append('неверно указан номер ЛР')

        validation_dictionary={ 
            'Number':1,
            'URL': "someurl.what",
            "errorDescription": Errors_list
            }

        answer = '- неверно указано название предмета'+"\n"+'- неверно указан номер ЛР'+"\n"

        get_error = error_in_work(validation_dictionary)

        self.assertEqual(get_error, answer)

    def test_send_message(self):

        from APIgoogle import send_message
        from APIgoogle import get_service
        from APIgoogle import get_message

        service = get_service()

        user_id = 'sanyabl.atchtozah.inya@gmail.com'
        email_of_student = 'sanyabl.atchtozah.inya@gmail.com'
        name_of_student = 'человек, который делает всё невовремя'
        number_of_templates = 1;

        Errors_list=[]
        Errors_list.append('неверно указан номер ЛР')
        validation_dictionary={ 
            'Number':1,
            'URL': "someurl.what",
            "errorDescription": Errors_list
            }

        send_message(service, user_id, email_of_student, name_of_student, number_of_templates, validation_dictionary)
        message_info = get_message(service, 'sanyabl.atchtozah.inya@gmail.com')

        search_id = service.users().messages().list(userId=user_id, labelIds = ['INBOX']).execute()
        message_id = search_id['messages']
        alone_msg = message_id[0]
        id_of_msg = alone_msg['id']
        hello_student = "Здравствуйте, " + name_of_student + "!"
        signature = " С уважением, Бот"
        our_msg = ' В Вашей работе обнаружены ошибки: ' + '- неверно указан номер ЛР '+ 'Просьба исправить их и отправить письмо повторно.'
        body_of_msg = hello_student + our_msg + signature

        our_info = {
            'id_of_msg':id_of_msg,
            'email_id':user_id,
            'head_of_msg':'Обнаружены ошибки в работе',
            'body_of_msg': body_of_msg
            }
        self.assertEqual(message_info, our_info)

if __name__ == '__main__':
    unittest.main()
