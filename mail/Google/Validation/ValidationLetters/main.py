import re


class ValidationMail():

    def __init__(self, subject, body):
        self.subject = subject
        self.body = body

    @staticmethod
    def validation_subject(subject):
        """
        Проверяет соответствие структуре темы. Включается в общий метод валидации
        :param subject: Тема письма
        :return: Успех валидации
        """
        subject = subject.lower()
        if subject[0:4] != "трпо":
            return False
        index = subject.find("лр", 0, 10)
        if index == -1:
            return False
        number_work = subject[index + 2:index + 5]
        if (number_work[0].isdigit() and number_work[1].isdigit()) or number_work[0].isdigit():
            return True
        else:
            number_work = number_work[1:3]
        if (number_work[0].isdigit() and number_work[1].isdigit()) or number_work[0].isdigit():
            return True
        else:
            return False

    @staticmethod
    def validation_body(body):
        """
        Проверяет соответствие структуре тела письма. Включается в общий метод валидации
        :param body: Тело письма
        :return: Успех валидации
        """
        salutation = ['здравствуйте', 'добрый', 'доброго', 'привет']
        links = []
        strings = body.split('\n')
        for item in strings:  # Убираю все лишнее
            if item == "" or item == "--" or item == '\r':
                strings.remove(item)
        hello = re.match(r'\w+', strings[0])
        hello = hello.group(0).lower()
        if (hello in salutation) is False:
            return False
        name = strings[len(strings) - 1]  # Это подпись
        res = re.match(r'\w+[ ]?\w+[, ]{2}\d{2}[-]?\w{4}[-]?\d\w', name)
        if res is None:
            return False
        for item in strings:  # Проверяю ссылки
            pattern = re.findall(r'https://[^ ]*', item)
            if len(pattern) != 0:
                links.append(pattern)
        if len(links) == 0:  # Если ссылок нет, то False
            return False
        return True

    def validation(self, subject, body):
        """
        Проверяет тему и тело письма на соответствие структуре
        :param subject: Тема письма
        :param body: Тело письма
        :return: Устпех валидации
        """
        if self.validation_subject(subject) is True and self.validation_body(body) is True:
            return True
        return False



