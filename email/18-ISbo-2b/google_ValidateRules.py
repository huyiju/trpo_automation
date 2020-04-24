import re


class ValidationMail():

    def __init__(self, subject, body):
        self.subject = subject
        self.body = body
        self.success = False

    @staticmethod
    def validation_subject(subject):
        """
        Проверяет соответствие структуре темы. Включается в общий метод валидации
        :param subject: Тема письма
        :return: Успех валидации
        """
        subject = subject.lower()
        if subject[0:4] != "трпо":
            return '02'
        variant = subject[-2:]
        if variant.isdigit() is not True:
            variant = variant[1]
        if variant.isdigit() is not True:
            return '02'
        index = subject.find("вар", 0, 30)
        if index == -1:
            return '02'
        index = subject.find("лр", 0, 10)
        if index == -1:
            return '02'
        number_work = subject[index + 2:index + 5]
        if (number_work[0].isdigit() and number_work[1].isdigit()) or number_work[0].isdigit():
            return '20'
        else:
            number_work = number_work[1:3]
        if (number_work[0].isdigit() and number_work[1].isdigit()) or number_work[0].isdigit():
            return '20'
        else:
            return '03'

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
            return '02'
        name = strings[len(strings) - 1]  # Это подпись
        res = re.match(r'\w+[ ]?\w+[, ]{2}\d{2}[-]?\w{4}[-]?\d\w', name)
        if res is None:
            return '02'
        for item in strings:  # Проверяю ссылки
            pattern = re.findall(r'https://[^ ]*', item)
            if len(pattern) != 0:
                links.append(pattern)
        if len(links) == 0:  # Если ссылок нет, то False
            return '03'
        return '20'

    def validation(self, subject, body):
        """
        Проверяет тему и тело письма на соответствие структуре
        :param subject: Тема письма
        :param body: Тело письма
        :return: Устпех валидации
        """
        if self.validation_subject(subject) == '20' and self.validation_body(body) == '20':
            self.success = True
            return '20'
        elif self.validation_subject(subject) == '20':
            return self.validation_body(body)
        else:
            return self.validation_subject(subject)

    def get_num_and_var(self, subject):
        if self.success is True:
            subject = subject.lower()
            var = subject[-2:]
            if var.isdigit() is not True:
                var = var[1]
            index = subject.find("лр", 0, 10)
            number_work = subject[index + 2:index + 5]
            if (number_work[0].isdigit() and number_work[1].isdigit()) or number_work[0].isdigit():
                if number_work[0].isdigit() and number_work[1].isdigit():
                    number_work = number_work[:2]
                else:
                    number_work = number_work[:1]
            else:
                number_work = number_work[1:3]
                if number_work[0].isdigit() and number_work[1].isdigit():
                    number_work = number_work[:2]
                else:
                    number_work = number_work[:1]

            return number_work, var
        else:
            return None
