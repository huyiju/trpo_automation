#include "functional.h"
#include "tcpserver.h"

/**
 * @brief Конструктор
 * @param parent - родитель этого класса, базовый QObject
 * @param linkLab - ссылка на репозиторий GitHub
 */
Functional::Functional(QString linkLab, QObject *parent) : QObject(parent)
{
    manager = new QNetworkAccessManager();
    link = linkLab;
    linkChange();

    connect(manager, &QNetworkAccessManager::finished, this, &Functional::slotCheckRepo);
}

/**
 * @brief Метод приводит ссылку к нужному виду
 * @return void
 */
void Functional::linkChange()
{
    link.insert(8, "api.");
    link.insert(23, "repos/");
    link.push_back("/contents");
}

/**
 * @brief Метод посылает GET запрос на GitHub и получает ответ в формате Json
 * @return void
 */
void Functional::getDataFromGithub()
{
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
    QByteArray jsonData, jsonData2;
    QJsonArray array;
    QString type;
    QString chek = "cpp";

    if  (reply->error() == QNetworkReply::NoError) {
        jsonData = reply->readAll();
        jsonData2 = jsonData;
        array = QJsonDocument::fromJson(jsonData).array();

        /* Проверяем что в репозитории находится только один файл */
        if (array.size() == 1) {
            for (const QJsonValue& value : array) {
                type = value.toObject() ["name"].toString();
            }

            /* Проверяем что это файл .cpp */
            if (type.indexOf(chek, -5) != -1) {

                /* Извлекаем ссылку */
                array = QJsonDocument::fromJson(jsonData).array();
                for (const QJsonValue& value : array) {
                    link = value.toObject() ["url"].toString();

                    /* Получаем данные файла #218 */
                }
            } else
                  qDebug() << "Error::TypeFile";
        } else
              qDebug() << "Error::NumberOfRepo";
    } else
          qDebug() << reply->error();
}

/**
 * @brief Метод разделяет полученный код на классы
 *        и помещает их в массив
 * @return void
 */
void Functional::dataProcessing()
{
    //Разделение кода на классы
}

/**
 * @brief Подчищаем за собой
 */
Functional::~Functional()
{
    delete manager;
}
