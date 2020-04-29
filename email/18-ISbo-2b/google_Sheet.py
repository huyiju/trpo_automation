"""
Подключение класса
"""

#Просто скопируйте это в вашу программу:

"""
from Sheet import Sheet
"""
# ---------------------------------------------------------------- #

"""
Вызов метода проверки email в базе.
возвращает bool или объект с ФИО студента!
"""

#Просто скопируйте это в вашу программу:

"""
email = 'test@gmail.com'    #замените здесь на ваши данные
result = Sheet.check_email(email)
"""
# ----------------------------------------------------------------- #

"""
Вызов метода выставления оценок.
возвращает bool!
"""

#Просто скопируйте это в вашу программу:

"""
first_name = 'Денисенко'    #замените здесь на ваши данные
surname = 'Мария'   #замените здесь на ваши данные
patronymic = 'Витальевна'   #замените здесь на ваши данные
group = '18-ИСбо-2б'    #замените здесь на ваши данные
lab_id = '5'   #id лаб. работы в журнале #замените здесь на ваши данные
value = 0 #оценка #замените здесь на ваши данные

result = Sheet.journal(group, first_name, surname, patronymic, lab_id, value)
"""


from google_Auth import Auth
import datetime
import re

class Sheet:

    def __init__(self):
        #Авторизация в сервисе
        self.service = Auth.auth_sheets()

    """
    #получение названия первого листа
    принимает ид-документа в гугл-таблицах
    возвращает
        название (или ид листа)
        bool - в случае ошибки

    !!!больше не используется, но полезен для понимания
    """
    #получение названия первого листа
    def sheet_name(spreadsheetId):
        try:
            service = Sheet().service
            
            # Получаем список листов, их Id и название
            spreadsheet = service.spreadsheets().get(spreadsheetId = spreadsheetId).execute()
            sheetList = spreadsheet.get('sheets')
            for sheet in sheetList:
                #sheet['properties']['sheetId'] # если понадобится id_листа
                sheet['properties']['title']
        
            sheet_name = sheetList[0]['properties']['title']
            return sheet_name
        except Exception:
            bool(0)

    
    """
    #чтение листа
        ********************
        * Описание метода: *
        ********************
        Если указан только sheet_name(имя листа)
            возвращает весь лист

        если дополнительно указан второй необязательный параметр,
            то возвращается содержимое запрошенной ячейки, т.е.
                diapazon_start - это адрес ячейки с которой начинается чтение, например,
                diapazon_start = "B2"

        * если дополнительно указан третий необязательный параметр,
            то возвращается содержимое запрошенного диапазона.
                diapazon_end - это конечный адрес выбираемого диапазона.
                Может иметь формат адреса ячейки, например, "D4".
                ** Или может являться просто названием столбца - "D",
                                                    или строки - "4"
            тогда будет возвращено все содержимое столбца / строки,
                            начиная с запрошенной начальной ячейки
        
        (*) Конечный диапазон должен быть больше начального

        (**)Это будет работать только в случае, если вы указываете
                в конечный диапазон тот же столбец, что и в начальном диапазоне,
                иначе третий параметр не будет обработан!

        !!! в случае исключения - возвращает bool
    """
    #чтение листа
    def read_sheet(spreadsheetId, sheet_name, diapazon_start = "", diapazon_end = ""):
        try:
            service = Sheet().service
            null_ptr = ""
            
            if diapazon_start != null_ptr:
                if diapazon_end != null_ptr:
                    ranges_str = sheet_name + "!" + diapazon_start + ":" + diapazon_end
                else: ranges_str = sheet_name + "!" + diapazon_start
            else: ranges_str = sheet_name

            ranges = [ranges_str]

            #ranges = ["Ответы на форму (1)!B2:B"] #Формат диапазона для запроса
                      
            results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                                 ranges = ranges, 
                                                 valueRenderOption = 'FORMATTED_VALUE',  
                                                 dateTimeRenderOption = 'FORMATTED_STRING').execute() 
            
            sheet_values = results['valueRanges'][0]['values']
            return sheet_values
        except Exception:
            return bool(0)

    """
    #Запись в конец листа
        принимает
            spreadsheetId = "id документа в гугл таблицах",
            ranges = 'Ответы на форму (1)', #название листа

            #объект
            body = {
                "range": "Ответы на форму (1)", #диапазон (добавление в конец этого листа)
                "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                "values": [
                            [today, email, surname, first_name, patronymic, group], # Заполняем первую строку
                            #[можем заполнить вторую и т.д. ],
                            #[today, email и т.п.- это переменные, содержащие строку]
                        ]
            }
            
        возвращает
            bool
    """
    #Запись в конец листа
    def append_sheet(spreadsheetId, ranges, body):
        try:
            service = Sheet().service
            value_input_option = 'USER_ENTERED'
            insert_data_option = 'INSERT_ROWS'
            value_range_body = body

            request = service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range=ranges, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
            response = request.execute()
            return bool(1)
        except Exception:
            return bool(0)

    """
    #заполнение ячейки
        принимает
            spreadsheetId = "id документа в гугл таблицах",
            ranges = 'Ответы на форму (1)', #диапазон
            value = '' #значение
            
        возвращает
            bool 
    """    
    #заполнение ячейки
    def update_sheet(spreadsheetId, ranges, value):
        try:
            service = Sheet().service
            results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
                "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
                "data": [
                    {"range": ranges,
                     "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                     "values": [
                                [value], # оценка
                               ]}
                ]
            }).execute()
            return bool(1)
        except Exception:
            return bool(0)


    """
    # Формирование данных и добавления записи в конец листа (регистрация студента)
        принимает
            spreadsheetId = 'id документа в гугл-таблицах',
            email = 'test@gmail.ru',
            group = '18-ИСбо-2б',
            first_name = 'имя',
            surname = 'фамилия',
            patronymic = 'отчество'
        возвращает
            bool
    """
    #Формирование данных и добавления записи в конец листа (регистрация студента)
    def new_student(spreadsheetId, email, group, first_name, surname, patronymic):
        today = datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S")
        
        ranges = 'Ответы на форму (1)'
        
        body = {
            "range": "Ответы на форму (1)", #диапазон 
            "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы#         "values": [
            "values": [
                        [today, email, surname, first_name, patronymic, group] # Заполняем строку
                    ]
            }
        
        result = Sheet.append_sheet(spreadsheetId, ranges, body) #Добавление записи в конец листа
        return result

    """
    # проверка наличия email в базе
        принимает email студента
        возвращает
            ФИО в формате: [['Фамилия', 'Имя', 'Отчество']]
            или bool (false), если email не найден
    """
    #проверка наличия email в базе
    def check_email(email):
        #ID документа в гугл-таблицах (список студентов)
        Email_sheetId = '1gMZiZqSE89vk3ZeYbTGYGaMMy7j-iMrYRjn-ECUhaag'
        
        sheet_name = 'Ответы на форму (1)' #имя листа
        
        d_start = "B1"  #начало диапазона
        d_end = "B" #конец диапазона
        
        #получаем все email из списка
        email_full = Sheet.read_sheet(Email_sheetId, sheet_name, d_start, d_end)
        if not email_full:
            return bool(0)
        
        #проверяем в базе
        number_str = Sheet.search_number_string(email_full, email)
        if not number_str:
            return bool(0)
        else:
            #Диапазон выставлен на ФИО студента
            start = 'C' + '{}'.format(number_str)
            end = 'E' + '{}'.format(number_str)
            student = Sheet.read_sheet(Email_sheetId, sheet_name, start, end)
            return student
    
    """
    # поиск листа по группе студента
        принимает
            spreadsheetId = "id документа в гугл-таблицах"
            group = '18-ИСбо-2б'
        возвращает
            название листа или bool
    """
    #поиск листа по группе студента
    def sheet_name_list(spreadsheetId, group):
        try:
            service = Sheet().service
        
            # Получаем список листов, их Id и название
            spreadsheet = service.spreadsheets().get(spreadsheetId = spreadsheetId).execute()
            sheetList = spreadsheet.get('sheets')
            for sheet in sheetList:
                match = re.search(group, sheet['properties']['title'])
                if match:
                    return sheet['properties']['title']
                #if not match:
                    #print('не найден')
                
        
            sheet_name = sheetList[0]['properties']['title']
            return sheet_name
        except Exception:
            return bool(0)
    
    """
    # добавление оценки в журнал
        принимает
            group = '18-ИСбо-2б',
            first_name = 'Фамилия',
            surname = 'Имя',
            patronymic = 'Отчество',
            lab_id = '14',   #id лаб. работы в журнале
            value = 0 #оценка
        возвращает
            bool
    """
    # добавление оценки в журнал
    def journal(group, first_name, surname, patronymic, lab_id, value):
        #ID документа в гугл-таблицах
        Journal_sheetId = '1MPkVTspH5MCtCvUXNTduhgQl90N3LIjzLjqfjYTDPdc'

        sheet_name = Sheet.sheet_name_list(Journal_sheetId, group) #имя листа
        #print(sheet_name)
        if not sheet_name:
            print(1)
            return bool(0)
        
        alfa = Sheet.search_for_id(Journal_sheetId, sheet_name, lab_id)
        if not alfa:
            print(2)
            return bool(0)

        number_str = Sheet.search_for_student(Journal_sheetId, sheet_name, first_name, surname, patronymic)
        
        if number_str:        
            #адрес ячейки для выставления оценки
            value_table = alfa + '{}'.format(number_str)
            #print(value_table)

            ranges = sheet_name + '!' + value_table
            result = Sheet.update_sheet(Journal_sheetId, ranges, value)

            return result
        else:
            print('нет строки')
            return bool(0)

    """
    #поиск адреса столбца по id лабы
        принимает
            Journal_sheetId = "id документа в гугл-таблицах", 
            sheet_name = "название листа",
            lab_id = "ИД номер лаб.работы"
        возвращает
           имя столбца или bool 
    """    
    #поиск адреса столбца по id лабы
    def search_for_id(Journal_sheetId, sheet_name, lab_id):
        d_start = "A1"  #начало диапазона
        d_end = "1" #конец диапазона
            
        #получаем всю строку с id из списка
        id_full = Sheet.read_sheet(Journal_sheetId, sheet_name, d_start, d_end)

        result = Sheet.search_alfa(id_full, lab_id)
        return result

    """
    #поиск адреса столбца в строке по шаблону
        принимает
            объект, содержащий ячейки в одной строке
            pattern - шаблон для поиска
        возвращает
           имя столбца или bool
    """    
    #поиск адреса столбца в строке по шаблону
    def search_alfa(full_str, pattern):
        alfa = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                  
        """ поиск адреса столбца по шаблону """
        count_pattern = full_str[0].count(pattern) # проверяем наличие ячейки (шаблона) в полученном объекте 
            
        #если шаблон найден, то получаем его индекс в списке
        if count_pattern != 0:
            index_pattern = full_str[0].index(pattern)

            a = index_pattern // len(alfa)
            b = index_pattern % len(alfa)

            S = ""  # сюда запишем адрес столбца
            if a < 1:
                S = alfa[b]
            else: 
                S = alfa[a-1] + alfa[b]
            return S
        
        return bool(0)

    """
    #поиск номера строки в журнале по ФИО студента
        принимает
            Journal_sheetId = "id документа в гугл-таблицах", 
            sheet_name = "название листа",
            first_name = "фамилия",
            surname = "имя",
            patronymic = "отчество"
        возвращает
            номер строки или bool 
    """
    #поиск номера строки в журнале по ФИО студента
    def search_for_student(Journal_sheetId, sheet_name, first_name, surname, patronymic):
        d_start = "D1"  #начало диапазона
        d_end = "D" #конец диапазона
            
        #получаем весь столбец с ФИО студентов из списка
        name_full = Sheet.read_sheet(Journal_sheetId, sheet_name, d_start, d_end)
        if not name_full:
            return bool(0)
        
        pattern = first_name + "\W+" + surname + "\W+" + patronymic #"\[\'" + email + "\'\]"        

        result = Sheet.search_number_string(name_full, pattern)
        return result

    """
    #поиск содержимого ячейки в столбце
        принимает
            объект, содержащий все значения в столбце
        возвращает
            номер строки, если шаблон найден
            bool (false), если шаблон не найден 
    """
    #поиск содержимого ячейки в столбце
    def search_number_string(full_column, pattern):
        for i in range(len(full_column)):
            value = ' '.join(map(str, full_column[i]))
            match = re.search(pattern, value)
            if match:
                number_str = i + 1     #номер строки
                #print(match[0])    #содержимое ячейки
                return number_str
        #print("pattern не найден")
        return bool(0)
        
