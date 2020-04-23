"""
Шаблоны для заполнения писем
"""


def funcSt(str_of_val_er, str_of_er):
    pattern = [
        {'title':'Работа успешно принята', 
         'our_msg':'Поздравляю!\nРабота успешно принята!' + 
                   '\nОценку можно проверить в журнале:' + 
                   '\nhttps://docs.google.com/spreadsheets/d/1gOX8T8ihy3J1' + 
                   'khhC16U1qDwaI-K6ndkp9LFWAHncuWA/edit?usp=sharing'},
        {'title':'Обнаружены ошибки в работе', 
         'our_msg':'В Вашей работе обнаружены ошибки:\n\n' + str_of_val_er + 
                   '\nПросьба исправить их и отправить письмо повторно.'},
        {'title':'Обнаружены ошибки в заполнении письма',
         'our_msg':'В структуре письма обнаружены следующие ошибки:\n\n' + 
                   str_of_er + '\nПросьба исправить их в соответствии с ' +
                   'документом\n' + 'https://docs.google.com/document/d/' + 
                   '1DRhgepxVwoscylIS2LCW-po5SFBdqOr-oo92bP_XfHE/edit?' + 
                   'usp=sharing'},
        {'title':'Авторизация пользователя',
         'our_msg':'Вы не найдены в системе. Пожалуйста, перейдите по' + 
                   ' ссылке и зарегистрируйтесь.\nhttps://docs.google.com' + 
                   '/forms/d/1nXhfOkE3KnWVFNzZ-jvvATAIb6T3zzwD5Ry8Itc-VmQ/' + 
                   'edit?usp=sharing'},
        {'title':'Ошибка модуля',
         'our_msg':'В модуле ... обнаружена ошибка. В ближайшее время ' + 
                   'роблема будет исправлена. Просим прощения за неудобства.'}]
    return pattern


def funcTs(name_of_student, validation_dictionary, str_of_er):
    pattern = [{'hello':'Здравствуйте, Юрий Викторович!\n\n',
                'title':'Ошибка в работе студента', 
                'our_msg':'Студент ' + name_of_student + 
                          ' не справился с задачей №' + 
                          validation_dictionary['Numder'] + 
                          ' (' + validation_dictionary['URL'] + ')' + 
                          '\nБыли допущены ошибки в работе:\n\n' +
                          str_of_er}, 
               {'hello':'Здравствуйте!', 
                'title':'Служба дала сбой',
                'our_msg':'В модуле ... возникла ошибка ...'}]
    return pattern


def funcHello(name_of_student):
    return f"Здравствуйте, {name_of_student}!\n\n"


GMAIL_OF_TRPO = "trpo.automation@gmail.com"


EMAIL_OF_TEACHER = 'yuri.silenok@gmail.com'


MAS_OF_TO = ['yuri.silenok@gmail.com', '0sashasmirnov0@gmail.com',
             'k.svyat395@gmail.com', 'MaXLyuT2000@gmail.com',
             'majishpro@gmail.com', 'Sirokko77@gmail.com',
             'nikita.lukyanow@gmail.com', 'generalgrigorevous@gmail.com', 
             'molchok.yurij@gmail.com', 'amr15319@gmail.com']


SIGNATURE = "\n\nС уважением,\nБот"
""""
Валидация
""""


SUBJECT_LIST = ['ТРПО'] # Список предметов
SUBJECTNUMBER_LIST = ['ЛР№1', 'Лабораторная работа №1', 
                      'ЛР№2', 'Лабораторная работа №2',
                      'ЛР№3', 'Лабораторная работа №3',
                      'ЛР№4', 'Лабораторная работа №4',
                      'ЛР№5', 'Лабораторная работа №5',
                      'ЛР№6', 'Лабораторная работа №6',
                      'ЛР№7', 'Лабораторная работа №7',
                      'ЛР№8', 'Лабораторная работа №8',
                      'ЛР№9', 'Лабораторная работа №9']
GREATING_LIST =  ['Добрый день','Добрый вечер'] # Список приветствий