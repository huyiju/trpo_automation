#include "functional.h"

/**
 * @brief Конструктор
 * @param parent - родитель этого класса, базовый QObject
 * @param linkLab - ссылка на репозиторий GitHub
 */
Functional::Functional(QObject *parent) : QObject(parent)
{
    manager = new QNetworkAccessManager();
    flag = true;

    connect(manager, &QNetworkAccessManager::finished, this, &Functional::slotCheckRepo);
}

/**
 * @brief Метод приводит ссылку к нужному виду
 * @return void
 */
void Functional::linkChange()
{    
    int index;
    const QString GITHUB = "github.com/";
    const QString HTTPS = "https://api.";

    index = link.indexOf(GITHUB, 0);
    link.insert(index, "api.");
    index = HTTPS.size() + GITHUB.size();
    link.insert(index, "repos/");
    link.push_back("/contents");
}

/**
 * @brief Метод посылает GET запрос на GitHub и получает ответ в формате Json
 * @return void
 */
void Functional::getDataFromGithub(QString linkLab)
{
    link = linkLab;
    if (flag) {
        linkChange();
    }
    QUrl url(link);
    QNetworkRequest request;
    request.setUrl(url);
    reply = manager->get(request);
}

/**
 * @brief Слот обрабатывает Json с GitHub'a
 * @return void
 */
void Functional::slotCheckRepo()
{
    QString message;

    if (reply->error() == QNetworkReply::NoError) {
        if (flag) {
            QString tempString;
            QByteArray jsonData;
            QJsonArray array;
            QString chek = "cpp";

            /* Индекс символа перед ".cpp" в наименовании файла (5 символ с конца)
               Используется для проверки типа файла */
            const int INDEX_FORMAT = -5;

            jsonData = reply->readAll();
            array = QJsonDocument::fromJson(jsonData).array();
            qDebug() << array;

            /* Ищем в репозитории файл .cpp */
            for (const QJsonValue& value : array) {
                tempString = value.toObject() ["name"].toString();

                if (tempString.indexOf(chek, INDEX_FORMAT) != -1) {
                    tempString = value.toObject() ["path"].toString();
                    link.push_back("/");
                    link.push_back(tempString);
                    break;
                }
            }

            /* Если в репозитории не был найден файл ".cpp" */
            if (tempString.indexOf(chek, INDEX_FORMAT) == -1) {
               message = "FileNotFound";
               emit Gateway::sendCheckResult(false, message);
         }

            /* Получаем данные файла #218 */
            flag = false;

        } else {
            /* Извлекаем код программы из Json объекта */
        }
    } else {
        message = reply->errorString();
        emit Gateway::sendCheckResult(false, message);

    }
}

/**
 * @brief Метод разделяет полученный код на классы
 *        и помещает их в массив
 * @return void
 */
void Functional::parseIntoClasses(QString link, QList<QString>* )
{
    getDataFromGithub(link);
    //Разделение кода на классы
}

/**
 * @brief Подчищаем за собой
 */
Functional::~Functional()
{
    delete manager;
}
