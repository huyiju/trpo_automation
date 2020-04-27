import unittest
import global_User as User
import global_Letter as Letter
import global_LetterResult as LetterResult
import base_WorkWithLetters
import socket
import global_LetterResult
import json
import select


class TestSendJSONForCheck(unittest.TestCase):

    def test_SendJSONForCheck_IsOk(self):
        student = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        letter = Letter.Letter(student, "ЛР01",
                               "Max", None)
        letters = []
        letters.append(letter)
        json1 = {
            "messageType": 1,
            "lab": 1,
            "variant": 1,
            "link": None,
            "code": "Max"
        }
        mystr = json.dumps(json1)
        jsonDates = []
        jsonDates.append(mystr)
        letterRes = LetterResult.LetterResult(student)
        letterRes.IsOK = True
        letterRes.VariantOfLab = 1
        letterRes.NumberOfLab = 1
        new_letters = []
        new_letters.append(letterRes)
        new_letters.append(base_WorkWithLetters.SendJSONForCheck(jsonDates, letters)[0])
        self.assertEqual(new_letters[1].IsOK, new_letters[0].IsOK)


    def test_SendJSONForCheck_Var(self):
        student = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        letter = Letter.Letter(student, "ЛР01",
                               "Max", None)
        letters = []
        letters.append(letter)
        json1 = {
            "messageType": 1,
            "lab": 1,
            "variant": 1,
            "link": None,
            "code": "Max"
        }
        mystr = json.dumps(json1)
        jsonDates = []
        jsonDates.append(mystr)
        letterRes = LetterResult.LetterResult(student)
        letterRes.IsOK = True
        letterRes.VariantOfLab = 1
        letterRes.NumberOfLab = 1
        new_letters = []
        new_letters.append(letterRes)
        new_letters.append(base_WorkWithLetters.SendJSONForCheck(jsonDates, letters)[0])
        self.assertEqual(new_letters[1].VariantOfLab, new_letters[0].VariantOfLab)


    def test_SendJSONForCheck_Number(self):
        student = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        letter = Letter.Letter(student, "ЛР01",
                               "Max", None)
        letters = []
        letters.append(letter)
        json1 = {
            "messageType": 1,
            "lab": 1,
            "variant": 1,
            "link": None,
            "code": "Max"
        }
        mystr = json.dumps(json1)
        jsonDates = []
        jsonDates.append(mystr)
        letterRes = LetterResult.LetterResult(student)
        letterRes.IsOK = True
        letterRes.VariantOfLab = 1
        letterRes.NumberOfLab = 1
        new_letters = []
        new_letters.append(letterRes)
        new_letters.append(base_WorkWithLetters.SendJSONForCheck(jsonDates, letters)[0])
        self.assertEqual(new_letters[1].NumberOfLab, new_letters[0].NumberOfLab)


if __name__ == "__main__":
    unittest.main()
