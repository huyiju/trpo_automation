# coding=utf-8
import global_User as User
import global_Letter as Letter

def create_letters():
    letters = []
    student = User.User("Максим Расторгуев", "18-ИСбо-2", "rastorguev10@gmail.com", True)
    body = """Доброго времени суток, Юрий Викторович!
Отправляю вам ссылку на репозиторий с выполненной 1-ой лабораторной:
https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01
--
С Уважением,
Расторгуев Максим, студент группы 18-ИСбо-2б"""
    letter = Letter.Letter(student, "ТРПО ЛР01 ВАР1", body, 1, 1)
    letters.append(letter)

    student = User.User("Валерий Бублин", "18-ИСбо-2", "valerabubla44@gmail.com", True)
    body = """Здравствуйте, Юрий Викторович!
Отправляю вам ссылку на репозиторий с выполненной 1-ой лабораторной:
https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01
--
С Уважением,
Валерий Бублин"""
    letter = Letter.Letter(student, "ТРПО ЛР02 ВАР1", body, 1, 1)
    letters.append(letter)

    student = User.User("Софья Безбрежанова", "18-ИСбо-2", "sofiebezcoast@gmail.com", False)
    body = """Добрый день, Юрий Викторович!
Как у вас дела?
С Уважением,
--
Софья Безбрежанова, студент группы 18-ИСбо-2б"""
    letter = Letter.Letter(student, "ТРПО ЛР01 ВАР2", body, 1, 1)
    letters.append(letter)

    student = User.User("Григорий Васверидзе", "18-ИСбо-2", "grishaakvasya@gmail.com", False)
    body = """Привет, Юра!
Отправляю вам ссылку на репозиторий с выполненной 1-ой лабораторной:
https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР01
С Уважением,
Григорий Васверидзе, студент группы 18-ИСбо-2б"""
    letter = Letter.Letter(student, "ТРПО ЛР01 ВАР3", body, 1, 1)
    letters.append(letter)

    student = User.User("Сантьяго Цеместес", "18-ИСбо-2", "santozemesjago@gmail.com", True)
    body = """Всем привет!
Отправляю вам ссылку на репозиторий с выполненной 2-ой лабораторной:
https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02
С Уважением,
--
Сантьяго Цеместес, студент группы 18-ИСбо-2б"""
    letter = Letter.Letter(student, "ТРПО ЛР01 ВАР4", body, 1, 1)
    letters.append(letter)

    student = User.User("Сантьяго Цеместес", "18-ИСбо-2", "santozemesjago@gmail.com", True)
    body = """Доброе утро!
Отправляю вам ссылку на репозиторий с выполненной 2-ой лабораторной:
https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02
С Уважением,
--
Сантьяго Цеместес, студент группы 18-ИСбо-2б"""
    letter = Letter.Letter(student, "ТРПО ЛР02 ВАР2", body, 2, 2)
    letters.append(letter)

    student = User.User("Борис Кипарис", "18-ИСбо-2", "kiparisforboris@gmail.com", True)
    body = """"Хаюшки, мистер ЮрВикт!
Отправляю вам ссылку на репозиторий с выполненной 2-ой лабораторной:
https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02
С Уважением,
--
Борис Кипарис, студент группы 18-ИСбо-2б"""
    letter = Letter.Letter(student, "ТРПО ЛР02 ВАР3", body, 2, 2)
    letters.append(letter)

    student = User.User("Сантьяго Цеместес", "18-ИСбо-2", "santozemesjago@gmail.com", True)
    body = """Доброго времени суток, Юрий Викторович!
Отправляю вам ссылку на репозиторий с выполненной 2-ой лабораторной:
А нет, не отправляю
С Уважением,
--
Сантьяго Цеместес, студент группы 18-ИСбо-2б"""
    letter = Letter.Letter(student, "ТРПО ЛР02 ВАР4", body, 2, 2)
    letters.append(letter)

    student = User.User("Санто Цеметретос", "18-ИСбо-2", "santozement322@gmail.com", True)
    body = """Доброго времени суток, Юрий Викторович!
Отправляю вам ссылку на репозиторий с выполненной 2-ой лабораторной:
https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2/ЛР02
С Уважением,
--
Здесь пригодилась бы подпись"""
    letter = Letter.Letter(student, "ТРПО ЛР02 ВАР1", body, 2, 2)
    letters.append(letter)

    student = User.User("Максим Расторгуев", "18-ИСбо-2", "rastorguev10@gmail.com", True)
    body = """Доброго времени суток, Юрий Викторович!
Отправляю вам ссылку на репозиторий с выполненной 1-ой лабораторной:
https://github.com/Progoger/TasksForStudents/tree/master/18-ИСбо-2
С Уважением,
--
Расторгуев Максим, студент группы 18-ИСбо-2б"""
    letter = Letter.Letter(student, "ТРПО ЛР01 ВАР2", body, 1, 1)
    letters.append(letter)

    return letters
