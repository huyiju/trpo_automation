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

    def tearDown(self):
        crypto.crypt_file('Example.json')
        crypto.crypt_file('config.py')
#сделать два метода с известным результатом
    def test_search_group(self):
        from config import SPREAD_SHEET_ID_INIT
        from config import CREDENTIALS_FILE
        from APIgoogle import search_group

        test_email = '0sashasmirnov0@gmail.com'
        act= ('18-ИСбо-2а', 'Смирнов Александр Алексеевич')
        exp = search_group(test_email)

        self.assertEqual(exp, act)

if __name__ == '__main__':
    unittest.main()
