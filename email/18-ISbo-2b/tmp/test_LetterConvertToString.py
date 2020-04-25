# coding=utf-8
import unittest
import global_User as User
import global_Letter as Letter
import LettersConvertToString

class MyTestCase(unittest.TestCase):
    def test_file_py(self):
        """Тест на файлы python"""
        "Входные данные"
        student = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1 = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2 = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters = []
        letter = Letter.Letter(student, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", None)
        letter1 = Letter.Letter(student1, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", None)
        letter2 = Letter.Letter(student2, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", None)

        letters.append(letter)
        letters.append(letter1)
        letters.append(letter2)
        letters = LettersConvertToString.LettersConvertToString(letters)

        list_body_input = [letters[0].Body, letters[1].Body, letters[2].Body]

        "Правильные данные"
        student_true = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1_true = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2_true = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters_true = []
        letter_true = Letter.Letter(student_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", None)
        letter_true.Body = "﻿Maxim_Rastorguev"
        letter1_true = Letter.Letter(student1_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", None)
        letter1_true.Body = "﻿Valeriy_Bublin"
        letter2_true = Letter.Letter(student2_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_py", None)
        letter2_true.Body = "﻿Artyom_Gusev"

        letters_true.append(letter_true)
        letters_true.append(letter1_true)
        letters_true.append(letter2_true)
        list_body_true = [letters_true[0].Body, letters_true[1].Body, letters_true[2].Body]

        self.assertEqual(list_body_input, list_body_true)

    def test_file_sln(self):
        """Тест на файлы sln"""
        "Входные данные"
        student = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1 = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2 = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters = []
        letter = Letter.Letter(student, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_sln", None)
        letter1 = Letter.Letter(student1, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_sln", None)
        letter2 = Letter.Letter(student2, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_sln", None)

        letters.append(letter)
        letters.append(letter1)
        letters.append(letter2)
        letters = LettersConvertToString.LettersConvertToString(letters)

        list_body_input = [letters[0].Body, letters[1].Body, letters[2].Body]

        "Правильные данные"
        student_true = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1_true = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2_true = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters_true = []
        letter_true = Letter.Letter(student_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_sln", None)
        letter_true.Body = "﻿Maxim_Rastorguev"
        letter1_true = Letter.Letter(student1_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_sln", None)
        letter1_true.Body = "﻿Valeriy_Bublin"
        letter2_true = Letter.Letter(student2_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_sln", None)
        letter2_true.Body = "﻿Artyom_Gusev"

        letters_true.append(letter_true)
        letters_true.append(letter1_true)
        letters_true.append(letter2_true)
        list_body_true = [letters_true[0].Body, letters_true[1].Body, letters_true[2].Body]

        self.assertEqual(list_body_input, list_body_true)
    def test_file_txt(self):
        """Тест на файлы txt"""
        "Входные данные"
        student = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1 = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2 = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters = []
        letter = Letter.Letter(student, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_txt", None)
        letter1 = Letter.Letter(student1, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_txt", None)
        letter2 = Letter.Letter(student2, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_txt", None)

        letters.append(letter)
        letters.append(letter1)
        letters.append(letter2)
        letters = LettersConvertToString.LettersConvertToString(letters)

        list_body_input = [letters[0].Body, letters[1].Body, letters[2].Body]

        "Правильные данные"
        student_true = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1_true = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2_true = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters_true = []
        letter_true = Letter.Letter(student_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_txt", None)
        letter_true.Body = "Maxim_Rastorguev"
        letter1_true = Letter.Letter(student1_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_txt", None)
        letter1_true.Body = "Valeriy_Bublin"
        letter2_true = Letter.Letter(student2_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01_test_txt", None)
        letter2_true.Body = "Artyom_Gusev"

        letters_true.append(letter_true)
        letters_true.append(letter1_true)
        letters_true.append(letter2_true)
        list_body_true = [letters_true[0].Body, letters_true[1].Body, letters_true[2].Body]

        self.assertEqual(list_body_input, list_body_true)

    def test_2files_1name(self):
        """Тест на 2 файла с одинаковым названием"""
        "Входные данные"
        student = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1 = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2 = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters = []
        letter = Letter.Letter(student, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_2files_1name", None)
        letter1 = Letter.Letter(student1, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_2files_1name", None)
        letter2 = Letter.Letter(student2, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_2files_1name", None)

        letters.append(letter)
        letters.append(letter1)
        letters.append(letter2)
        letters = LettersConvertToString.LettersConvertToString(letters)

        list_body_input = [letters[0].Body, letters[1].Body, letters[2].Body]

        "Правильные данные"
        student_true = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1_true = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2_true = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters_true = []
        letter_true = Letter.Letter(student_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_2files_1name", None)
        letter_true.Body = ""
        letter1_true = Letter.Letter(student1_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_2files_1name", None)
        letter1_true.Body = ""
        letter2_true = Letter.Letter(student2_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_2files_1name", None)
        letter2_true.Body = "﻿Artyom_Gusev_file_slnArtyom_Gusev_file_txt"

        letters_true.append(letter_true)
        letters_true.append(letter1_true)
        letters_true.append(letter2_true)
        list_body_true = [letters_true[0].Body, letters_true[1].Body, letters_true[2].Body]

        self.assertEqual(list_body_input, list_body_true)

    def test_file_error(self):
        """Тест на отсутствие файла"""
        "Входные данные"
        student = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1 = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2 = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters = []
        letter = Letter.Letter(student, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_file_error", None)
        letter1 = Letter.Letter(student1, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_file_error", None)
        letter2 = Letter.Letter(student2, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_file_error", None)

        letters.append(letter)
        letters.append(letter1)
        letters.append(letter2)
        letters = LettersConvertToString.LettersConvertToString(letters)

        list_body_input = [letters[0].Body, letters[1].Body, letters[2].Body]

        "Правильные данные"
        student_true = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1_true = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2_true = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters_true = []
        letter_true = Letter.Letter(student_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_file_error", None)
        letter_true.Body = '﻿Maxim_Rastorguev'
        letter1_true = Letter.Letter(student1_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_file_error", None)
        letter1_true.Body = "﻿Valeriy_Bublin"
        letter2_true = Letter.Letter(student2_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_file_error", None)
        letter2_true.Body = ""

        letters_true.append(letter_true)
        letters_true.append(letter1_true)
        letters_true.append(letter2_true)
        list_body_true = [letters_true[0].Body, letters_true[1].Body, letters_true[2].Body]

        self.assertEqual(list_body_input, list_body_true)

    def test_incorrect_name(self):
        """Тест на корректность имени/фамилии"""
        "Входные данные"
        student = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1 = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2 = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters = []
        letter = Letter.Letter(student, "ЛР01","https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_incorrect_name", None)
        letter1 = Letter.Letter(student1, "ЛР01","https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_incorrect_name", None)
        letter2 = Letter.Letter(student2, "ЛР01","https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_incorrect_name", None)

        letters.append(letter)
        letters.append(letter1)
        letters.append(letter2)
        letters = LettersConvertToString.LettersConvertToString(letters)

        list_body_input = [letters[0].Body, letters[1].Body, letters[2].Body]

        "Правильные данные"
        student_true = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1_true = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2_true = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters_true = []
        letter_true = Letter.Letter(student_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_incorrect_name", None)
        letter_true.Body = ""
        letter1_true = Letter.Letter(student1_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_incorrect_name", None)
        letter1_true.Body = ""
        letter2_true = Letter.Letter(student2_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_incorrect_name", None)
        letter2_true.Body = ""

        letters_true.append(letter_true)
        letters_true.append(letter1_true)
        letters_true.append(letter2_true)
        list_body_true = [letters_true[0].Body, letters_true[1].Body, letters_true[2].Body]

        self.assertEqual(list_body_input, list_body_true)

    def test_name_reverse(self):
        """Тест на фамилия имя (а не имя фамилия)"""
        "Входные данные"
        student = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1 = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2 = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters = []
        letter = Letter.Letter(student, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_name_reverse", None)
        letter1 = Letter.Letter(student1, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_name_reverse", None)
        letter2 = Letter.Letter(student2, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_name_reverse", None)

        letters.append(letter)
        letters.append(letter1)
        letters.append(letter2)
        letters = LettersConvertToString.LettersConvertToString(letters)

        list_body_input = [letters[0].Body, letters[1].Body, letters[2].Body]

        "Правильные данные"
        student_true = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1_true = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2_true = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters_true = []
        letter_true = Letter.Letter(student_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_name_reverse", None)
        letter_true.Body = ""
        letter1_true = Letter.Letter(student1_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_name_reverse", None)
        letter1_true.Body = "﻿Valeriy_Bublin"
        letter2_true = Letter.Letter(student2_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_name_reverse", None)
        letter2_true.Body = ""

        letters_true.append(letter_true)
        letters_true.append(letter1_true)
        letters_true.append(letter2_true)
        list_body_true = [letters_true[0].Body, letters_true[1].Body, letters_true[2].Body]

        self.assertEqual(list_body_input, list_body_true)

    def test_no_family(self):
        """Тест на отсутствие фамилии"""
        "Входные данные"
        student = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1 = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2 = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters = []
        letter = Letter.Letter(student, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_no_family", None)
        letter1 = Letter.Letter(student1, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_no_family", None)
        letter2 = Letter.Letter(student2, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_no_family", None)

        letters.append(letter)
        letters.append(letter1)
        letters.append(letter2)
        letters = LettersConvertToString.LettersConvertToString(letters)

        list_body_input = [letters[0].Body, letters[1].Body, letters[2].Body]

        "Правильные данные"
        student_true = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1_true = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2_true = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters_true = []
        letter_true = Letter.Letter(student_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_no_family", None)
        letter_true.Body = "﻿Maxim_Rastorguev"
        letter1_true = Letter.Letter(student1_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_no_family", None)
        letter1_true.Body = ""
        letter2_true = Letter.Letter(student2_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_no_family", None)
        letter2_true.Body = ""

        letters_true.append(letter_true)
        letters_true.append(letter1_true)
        letters_true.append(letter2_true)
        list_body_true = [letters_true[0].Body, letters_true[1].Body, letters_true[2].Body]

        self.assertEqual(list_body_input, list_body_true)

    def test_no_name(self):
        """Тест на отсутствие имени"""
        "Входные данные"
        student = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1 = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2 = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters = []
        letter = Letter.Letter(student, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_no_name", None)
        letter1 = Letter.Letter(student1, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_no_name", None)
        letter2 = Letter.Letter(student2, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_no_name", None)

        letters.append(letter)
        letters.append(letter1)
        letters.append(letter2)
        letters = LettersConvertToString.LettersConvertToString(letters)

        list_body_input = [letters[0].Body, letters[1].Body, letters[2].Body]

        "Правильные данные"
        student_true = User.User("Максим Расторгуев", "18-ИСбо-2", None, None)
        student1_true = User.User("Валерий Бублин", "18-ИСбо-2", None, None)
        student2_true = User.User("Артём Гусев", "18-ИСбо-2", None, None)
        letters_true = []
        letter_true = Letter.Letter(student_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_no_name", None)
        letter_true.Body = "﻿Maxim_Rastorguev"
        letter1_true = Letter.Letter(student1_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_no_name", None)
        letter1_true.Body = ""
        letter2_true = Letter.Letter(student2_true, "ЛР01", "https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02_test_no_name", None)
        letter2_true.Body = ""

        letters_true.append(letter_true)
        letters_true.append(letter1_true)
        letters_true.append(letter2_true)
        list_body_true = [letters_true[0].Body, letters_true[1].Body, letters_true[2].Body]

        self.assertEqual(list_body_input, list_body_true)

if __name__ == '__main__':
    unittest.main()
