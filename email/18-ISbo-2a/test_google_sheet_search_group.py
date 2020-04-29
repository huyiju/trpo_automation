import unittest
import httplib2
import requests
import Decode
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

class Test_google(unittest.TestCase):
        
    def setUp(self):
        Decode.Decode_config('config.py.bak', ['SPREAD_SHEET_ID', 'SPREAD_SHEET_ID_INIT', 'CREDENTIALS_FILE'])
        Decode.Decode_files(['Example.json.bak'])

    def tearDown(self):
        Decode.Finish(['config.py.bak', 'Example.json.bak'])
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
