import unittest
import crypto
class Test_google(unittest.TestCase):
    def setUp(self):
        crypto.decrypt_file('Example.json.bin')
        crypto.decrypt_file('config.py.bin')

    def tearDown(self):
        crypto.crypt_file('Example.json')
        crypto.crypt_file('config.py')

    def test_search_tablic(self):
        from APIgoogle import search_tablic
        act=search_tablic('18-Исбо-2а','7','Лютый Максим Сергеевич')
        exp='P6'
        self.assertEqual(act, exp)
    def test_search_tablic1(self):
        from APIgoogle import search_tablic
        act=search_tablic('18-Исбо-2б','7','Лютый Максим Сергеевич')
        self.assertIsNone(act)
    def test_search_tablic2(self):
        from APIgoogle import search_tablic
        act=search_tablic('18-Исбо-2а','','Лютый Максим Сергеевич')
        self.assertIsNone(act)
    def test_search_tablic3(self):
        from APIgoogle import search_tablic
        act=search_tablic('18-Исбо-2а','7','Смирнов Александр Алексеевич')
        exp='P9'
        self.assertEqual(act, exp)
    def test_search_tablic4(self):
        from APIgoogle import search_tablic
        act=search_tablic('18-Исбо-2а','7','')
        self.assertIsNone(act)
        


if __name__ == '__main__':
    unittest.main()
