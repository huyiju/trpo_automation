#!/usr/bin/python
# -*- coding: utf-8 -*-
# from Validation import User
# from Validation import Letter

def CheckEmail():
    """
    Точка входа в работу модуля
    """

    print("letters = GetLetters()")
    """
    Функционал:
    - Прочитать письма на почте 
    - Пометить прочитанные письма метками
    На входе: 
    - None
    На выходе:
    - letters - объект, содержащий письма
    Что предусмотреть:
    - None
    Участвующие внешние типы переменных
    - None
    """

    print("SetTimer()")
    """
    Функционал:
    - Поставить таймер на необходимое время, 
    На входе:
    - None
    На выходе:
    - Установленный экземпляр таймера (глобальная переменная)
    Что предусмотреть:
    - Внутри должно происходить обращение к глобальной переменной, в которой хранится таймер и информация по времени 
    таймера должна содержаться в самом таймере
    Участвующие внешние типы переменных
    - global timer
    """

    print("GetReserveDate()")
    """
    Функционал:
    - Получить резервные данные для восстановления
    В зависимости от выбранного подхода это:
    - - Либо данные по двум журналам - доступа и оценок
    - - Либо номера версий журналов
    На входе:
    - None
    На выходе:
    - Копии журналов / номера версий журналов (глобальные переменные)
    Что предусмотреть:
    - None
    Участвующие внешние типы переменных
    - global version_assess / journal_assess
    - global version_marks / journal_marks
    """

    print("letters = FormListWithLetters(letters)")
    """
    Функционал:
    - Сформировать список экземпляров класса Letter на основе сырых данных по письмам
    На входе:
    - Объект с сырыми данными по письмам
    На выходе:
    - Список экземпляров класса Letter
    Что предусмотреть:
    - Парсинг сырых данных
    - Декодирование сырых данных
    - Заполнение всех полей в Letter на основе обработанной информации кроме 'Code' и 'CodeComment' 
    - Поля 'Code' и 'CodeComment' заполняются только в случае существующего приложения к письму (что противоречит
     правилам отправки писем)
    - Заполнение поля User - вытаскивание всех данных о конкретном пользователе (кроме поля isRegistered)
    Участвующие внешние типы переменных
    - User (from import)
    - Letter (from import)
    """

    print("CheckUsers(letters)")
    """
    Функционал:
    - Проверить зарегистрированность каждого пользователя в системе по email
    На входе:
    - Список писем
    На выходе:
    - Расставленное поле 'isRegistered' в каждом письме в поле 'User'
    Что предусмотреть:
    - None
    Участвующие внешние типы переменных
    - None
    """

    print("ValidateLetters(letters)")
    """
    Функционал:
    - Провалидировать каждое письмо по правилам валидации
    На входе:
    - Список писем
    На выходе:
    - Расставленные поля 'Code' и 'CodeComment' в каждом письме 
    Что предусмотреть:
    - Просле проверки вытащить ссылки на ресурсы и поместить их в поле 'Body' каждого письма
    - Проверку выполнять только если поле 'Code' ещё не заполнено 
    - Поле 'CodeComment' заполнять сокращённой информацией по результатам проверки как угодно.     
    Участвующие внешние типы переменных
    - None
    """

    print("WorkWithLetters(letters)")




# if __name__ == "__main__":
#     CheckEmail()