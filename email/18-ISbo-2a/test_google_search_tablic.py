import unittest
import Decode
class Test_google(unittest.TestCase):
    def setUp(self):
        Decode.Decode_config('config.py.bak', ['SPREAD_SHEET_ID', 'CREDENTIALS_FILE'])
        Decode.Decode_files(['Example.json.bak'])

    def tearDown(self):
        Decode.Finish(['config.py', 'Example.json'])

    def test_search_tablic(self):
        from APIgoogle import search_tablic
        act=search_tablic('18-Исбо-2а','7','Лютый Максим Сергеевич')
        exp='P6'
        self.assertEqual(act, exp)
    def test_search_tablic1(self):
        from APIgoogle import search_tablic
        act=search_tablic('18-Исбо-2б','7','Лютый Максим Сергеевич')
        self.assertNone(act)
    def test_search_tablic2(self):
        from APIgoogle import search_tablic
        act=search_tablic('18-Исбо-2а','','Лютый Максим Сергеевич')
        self.assertNone(act)
    def test_search_tablic3(self):
        from APIgoogle import search_tablic
        act=search_tablic('18-Исбо-2а','7','Смирнов Александр Алексеевич')
        exp='P9'
        self.assertEqual(act, exp)
    def test_search_tablic4(self):
        from APIgoogle import search_tablic
        act=search_tablic('18-Исбо-2а','7','')
        self.assertNone(act)
        


if __name__ == '__main__':
    unittest.main()
