# Подключаем библиотеки
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

class Auth:
    """Авторизация в системе, выбор API для работы с Google Sheets """

    def auth_sheets():
        CREDENTIALS_FILE = 'trpo-bot-1eb977889b18.json'  # Имя файла с закрытым ключом, вы должны подставить свое

        # servis email: trpo-bot@trpo-bot.iam.gserviceaccount.com
        # Читаем ключи из файла
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
        return service
