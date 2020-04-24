# coding=utf-8
from User import User
from Letter import Letter
from Validation.main import *


def CheckEmail():

    print("Иммитирую возврат метода проверки почты")
    obj1 = r"""Здравствуйте
https://github.com/Students-of-the-city-of-Kostroma/trpo_automation/issues/88
Ельцов Андрей, 18-ИСбо-2б"""
    obj2 = r"""Ку
    https://github.com/Students-of-the-city-of-Kostroma/trpo_automation/issues/88
    Ельцов Андрей, 18-ИСбо-2б"""
    us1 = User("Вася", "18-is", "aa2@mail.ru", True)
    us2 = User("Коля", "18-id", "bb4@mail.ru", True)
    let1 = Letter(us1, "ТРПО ЛР10 Название", obj1)
    let2 = Letter(us2, "ТРПО ЛР10 Название", obj2)
    letters = [let1, let2]  # Письма с почты. Результат работы метода проверки почты
    print(letters)
    print("Метод вернул этот список")
    answer = []  # Список с ответами пользователю
    print("Начинаю проверять письма")
    for let in letters:
        val = ValidationMail(let.ThemeOfLetter, let.Body)
        let.CodeStatus = val.validation(val.subject, val.body)
        print("Заполнил поле CodeStatus")
        print("Поле CodeStatusComment вызывает вопросы")
        # let.CodeStatusComment = Как назначать?
        if let.CodeStatus != '20':
            letters.remove(let)
            print("Удалил письмо по причине " + let.CodeStatus)
        else:
            let.Body = re.findall(r'https://[^ \n]*', let.Body)
            print("В теле оставил только ссылку\n" + str(let.Body))
            answer.append(str(let.Student) + '_' + str(let.CodeStatus))  # Ответ пользователям в виде ИМЯ_Код
            print("На всякий случай сформировал список ответов пользователю в виде ИМЯ_Код")
            print("Обработал письмо. Беру новое")

    # WorkWithLetters(letters)




