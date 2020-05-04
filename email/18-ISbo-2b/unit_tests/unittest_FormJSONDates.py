import json
import unittest
import global_User as User
import global_Letter as Letter
import FormJSONDates


class MyTestCase(unittest.TestCase):
    """Тестирование метода FormJSONDates"""

    def test_function(self):
        """Тест на общий функционал"""
        student1 = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student2 = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student3 = User.User("Артём Гусев", "18-ИСбо-2", None, None)

        letters = []
        letter1 = Letter.Letter(student1, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", 1, 1)
        letter1.Body = "Maxim_Rastorguev"
        letter1.CodeStatus = "20"
        letter2 = Letter.Letter(student2, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", 2, 1)
        letter2.Body = "Valeriy_Bublin"
        letter2.CodeStatus = "20"
        letter3 = Letter.Letter(student3, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", 3, 1)
        letter3.Body = "Artyom_Gusev"
        letter3.CodeStatus = "20"

        letters.append(letter1)
        letters.append(letter2)
        letters.append(letter3)

        jsonDates_received = FormJSONDates.FormJSONDates(letters)

        json1_expected = {
                "messageType" : 1,
                "lab" : 1,
                "variant" : 1,
                "link" : None,
                "code" : "Maxim_Rastorguev"
                }
        json2_expected = {
                "messageType" : 1,
                "lab" : 1,
                "variant" : 2,
                "link" : None,
                "code" : "Valeriy_Bublin"
                }
        json3_expected = {
                "messageType" : 1,
                "lab" : 1,
                "variant" : 3,
                "link" : None,
                "code" : "Artyom_Gusev"
                }

        jsonDates_expected = [json.dumps(json1_expected), json.dumps(json2_expected), json.dumps(json3_expected)]

        self.assertEqual(jsonDates_received, jsonDates_expected)

    def test_CodeStatus(self):
        """Тест на фильтрацию по CodeStatus"""
        student1 = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student2 = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student3 = User.User("Артём Гусев", "18-ИСбо-2", None, None)

        letters = []
        letter1 = Letter.Letter(student1, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", 16, 1)
        letter1.Body = "Maxim_Rastorguev"
        letter1.CodeStatus = "03"
        letter2 = Letter.Letter(student2, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", 2, 1)
        letter2.Body = "Valeriy_Bublin"
        letter2.CodeStatus = "20"
        letter3 = Letter.Letter(student3, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", 3, 1)
        letter3.Body = "Artyom_Gusev"
        letter3.CodeStatus = "20"

        letters.append(letter1)
        letters.append(letter2)
        letters.append(letter3)

        jsonDates_received = FormJSONDates.FormJSONDates(letters)

        json2_expected = {
                "messageType" : 1,
                "lab" : 1,
                "variant" : 2,
                "link" : None,
                "code" : "Valeriy_Bublin"
                }
        json3_expected = {
                "messageType" : 1,
                "lab" : 1,
                "variant" : 3,
                "link" : None,
                "code" : "Artyom_Gusev"
                }

        jsonDates_expected = [json.dumps(json2_expected), json.dumps(json3_expected)]

        self.assertEqual(jsonDates_received, jsonDates_expected)

    def test_function(self):
        """Тест на общий функционал"""
        student1 = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student2 = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student3 = User.User("Артём Гусев", "18-ИСбо-2", None, None)

        letters = []
        letter1 = Letter.Letter(student1, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", 1, 1)
        letter1.Body = "Maxim_Rastorguev"
        letter1.CodeStatus = "20"
        letter2 = Letter.Letter(student2, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", 2, 1)
        letter2.Body = "Valeriy_Bublin"
        letter2.CodeStatus = "20"
        letter3 = Letter.Letter(student3, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", 3, 1)
        letter3.Body = "Artyom_Gusev"
        letter3.CodeStatus = "20"

        letters.append(letter1)
        letters.append(letter2)
        letters.append(letter3)

        jsonDates_received = FormJSONDates.FormJSONDates(letters)

        json1_expected = {
                "messageType" : 1,
                "lab" : 1,
                "variant" : 1,
                "link" : None,
                "code" : "Maxim_Rastorguev"
                }
        json2_expected = {
                "messageType" : 1,
                "lab" : 1,
                "variant" : 2,
                "link" : None,
                "code" : "Valeriy_Bublin"
                }
        json3_expected = {
                "messageType" : 1,
                "lab" : 1,
                "variant" : 3,
                "link" : None,
                "code" : "Artyom_Gusev"
                }

        jsonDates_expected = [json.dumps(json1_expected), json.dumps(json2_expected), json.dumps(json3_expected)]

        self.assertEqual(jsonDates_received, jsonDates_expected)

if __name__ == '__main__':
    unittest.main()
