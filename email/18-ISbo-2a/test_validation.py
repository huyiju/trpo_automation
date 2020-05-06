import unittest

class Test_validation(unittest.TestCase):

    def test_urlcheack1(self):

        from Validation import url_cheack

        body_of_msg = 'Добрый день! http://github.com.'
        number = '8'

        URL = url_cheack(number, body_of_msg)

        self.assertEqual(URL, 'http://github.com')

    def test_urlcheack2(self):

        from Validation import url_cheack

        body_of_msg = 'Добрый день! http://github.com.'
        number = '6'

        URL = url_cheack(number, body_of_msg)

        self.assertIsNone(URL)

    def test_urlcheack3(self):

        from Validation import url_cheack

        body_of_msg = 'Добрый день! http://github.com - ссылка на репозиторий.'
        number = '8'

        URL = url_cheack(number, body_of_msg)

        self.assertEqual(URL, 'http://github.com')

    def test_urlcheack4(self):

        from Validation import url_cheack

        body_of_msg = 'Добрый день! htp://github.com.'
        number = '8'

        URL = url_cheack(number, body_of_msg)

        self.assertIsNone(URL)
    
    def test_validation1(self):

        from Validation import validation

        head_of_msg = 'ТРПО ЛР№1'
        body_of_msg = 'Добрый день! Вот ссылка на гитхаб - http://github.com. --подпись типа'       
        validation_dictionary={ 
            'Number':'1',
            'URL': None,
            "errorDescription": []
            }

        answer = validation(head_of_msg, body_of_msg)

        self.assertEqual(answer, validation_dictionary)
    
    def test_validation2(self):

        from Validation import validation

        head_of_msg = 'ТИПИС ЛР 1'
        body_of_msg = 'Салют! Вот ссылка на гитхаб - http://github.com. Кандидат на отчисление'
        Errors_list = []
        Errors_list.append('неверно указано название предмета')
        Errors_list.append('неверно указан номер ЛР')
        Errors_list.append('отсутствует приветствие')
        Errors_list.append('отсутствует подпись')
        validation_dictionary={ 
            'Number':None,
            'URL': None,
            "errorDescription": Errors_list
            }

        answer = validation(head_of_msg, body_of_msg)

        self.assertEqual(answer, validation_dictionary)
    
    def test_validation3(self):

        from Validation import validation

        head_of_msg = 'ТРПО ЛР№8'
        body_of_msg = 'Салют! Вот ссылка на гитхаб - http://github.com.'
        Errors_list = []
        Errors_list.append('отсутствует приветствие')
        Errors_list.append('отсутствует подпись')
        validation_dictionary={ 
            'Number':'8',
            'URL': 'http://github.com',
            "errorDescription": Errors_list
            }

        answer = validation(head_of_msg, body_of_msg)

        self.assertEqual(answer, validation_dictionary)

if __name__ == '__main__':
    unittest.main()
