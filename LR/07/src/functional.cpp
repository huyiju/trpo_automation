#include "functional.h"

/**
 * @brief Конструктор
 * @param parent - родитель этого класса, базовый QObject
 * @param linkLab - ссылка на репозиторий GitHub
 */
Functional::Functional(QObject *parent)
    : QObject(parent),
      manager(new QNetworkAccessManager())
{
    if (manager->networkAccessible()
          == QNetworkAccessManager::UnknownAccessibility) {
        manager->setNetworkAccessible(QNetworkAccessManager::Accessible);
    }
}

/**
 * @brief Метод формирования и выполнения GET запроса через API Github
 * @param path - относительный путь API Github
 * @param callback - функция, которую надо будет вызывать после обработки
 * @return
 */
void Functional::getRequest(QUrl path, const std::function<void(QJsonDocument)> &callback)
{
    QEventLoop wait;

    // формируем запрос
    QNetworkRequest request(GITHUB_URL + "/" + path.toString());
    request.setHeader(QNetworkRequest::UserAgentHeader, USER_AGENT);
    request.setRawHeader("Accept", "application/vnd.github.v3+json");
    QNetworkReply *reply = manager->get(request);

    // ждем ответа
    connect(reply, SIGNAL(finished()), &wait, SLOT(quit()));
    wait.exec();

    // обрабатываем ответ
    callback(handleReply(reply));
    reply->deleteLater();
}

/**
 * @brief Обработчик успешного выполнения запроса
 * @param req - структура запроса
 * @return
 */
QJsonDocument Functional::handleReply(QNetworkReply *reply)
{
    int statusCode = reply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();
    if (statusCode == 200) {
        QByteArray data = reply->readAll();
        if (data.isNull() || data.isEmpty() || (strcmp(data.constData(), "null") == 0)) {
            return QJsonDocument();
        }

        QJsonParseError parseError;
        QJsonDocument replyData = QJsonDocument::fromJson(data, &parseError);

        if (parseError.error != QJsonParseError::NoError) {
            throw SystemException("parse error for Github reply on get reuest", parseError.errorString());
        }

        return replyData;
    }

    QString reason = reply->attribute(QNetworkRequest::HttpReasonPhraseAttribute).toString();
    throw SystemException("Not successful request on Github.\nStatus code: " + QString::number(statusCode), reason);
}

/**
 * @brief Метод получения имени файла .cpp в репозитории
 * @param jsonArray - Json массив, где содержатся объекты
 *          с информацией о фалйах в репозитории
 * @param fileName - ссылка на имя файла
 * @return
 */
void Functional::getFileInside(QJsonArray jsonArray, QString& fileName)
{
    foreach (QJsonValue value, jsonArray) {
        QFileInfo file = value.toObject()["name"].toString();
        if (file.suffix() == FILE_EXTENSION) {
            fileName = file.fileName();
        }
    }
}

/**
 * @brief Метод приводит ссылку к нужному виду
 * @return QUrl
 */
QUrl Functional::linkChange(QString &link)
{

    QString repoName = link.mid(link.lastIndexOf("/"));
    link = link.remove(repoName);
    QString repoOwner = link.mid(link.lastIndexOf("/"));
    return QUrl("repos" + repoOwner + repoName + "/contents");
}

/**
 * @brief Метод извлекает код программы из Json
 * @param reply - Json, который присылает GitHub
 * @return QString
 */
QString Functional::getCode(QJsonDocument reply)
{
    QJsonObject object = reply.object();
    QString tempString = object.take("content").toString();

    QByteArray jsonData;
    jsonData.clear();
    jsonData.append(tempString);
    tempString = jsonData.fromBase64(jsonData).data();
    return tempString;
}

/**
 * @brief Метод разделяет полученный код на классы
 *        и помещает их в массив
 * @return void
 */
void Functional::parseIntoClasses(QString contentCode, QList<QString>* ListOfClasses)
{
    code = contentCode;
    QString addToList;
    int firstIndex = 0, secondIndex = 0, addToListIndex = 0;

    QString mainFunction = findMainFunc();
    ListOfClasses->append(mainFunction);

    while ((code.indexOf("class", firstIndex)) >= 0) {
        firstIndex = code.indexOf("class", firstIndex);
        secondIndex = (code.indexOf("};", secondIndex))+1;

        QString className = findNameOfClass(firstIndex+5);

        for (; firstIndex <= secondIndex; firstIndex++) {
            addToList[addToListIndex] = code[firstIndex];
            addToListIndex++;
        }
        QString classMethods = findClassMethods(className, secondIndex);
        addToList += classMethods;
        addToListIndex = 0;
        ListOfClasses->append(addToList);
        addToList.clear();

        firstIndex = secondIndex;
    }
}
/**
 * @brief   Метод ищет название класса
 * @param   firstIndex - индекс, указывающий на пробел перед названием класса
 * @return  возвращает название класса
 */

QString Functional::findNameOfClass(int firstIndex)
{
    QString className;
    int i = 0;
    while (code[firstIndex] == ' ') {
        firstIndex++;
    }
    while (code[firstIndex] != ' ') {
        if (code[firstIndex] == '{') {
            return className;
        }
        else {
        className[i] = code[firstIndex];
        firstIndex++;
        i++;
        }
    }
    return className;
}
/**
 * @brief   Метод находит методы определенного класса, если они написаны не внутри него
 * @param   className - название класса
 * @param   startIndex - начальный индекс, отсюда начнется поиск методов
 * @return  возвращает строку со всеми найденными методами или пустую строку, если методов нет
 */
QString Functional::findClassMethods(QString className, int startIndex)
{
    int sIndexForMethod=0, i=0, firstIndex=0;
    QString classMethods;
        while ((code.indexOf(className, startIndex)) >= 0) {
            firstIndex = code.indexOf(className, startIndex);
            if ((code[firstIndex + className.size()] == ' ') || (code[firstIndex + className.size()] == ':')) {
            while ((code.indexOf("\n", startIndex) < firstIndex) && (code.indexOf("\n", startIndex)) != -1) {
                sIndexForMethod = (code.indexOf("\n", startIndex))+1;
                startIndex = sIndexForMethod;
            }
            if (sIndexForMethod != 0) {
                while (code[sIndexForMethod] != '{') {
                    classMethods[i] = code[sIndexForMethod];
                    i++;
                    sIndexForMethod++;
                }
                classMethods[i] = code[sIndexForMethod];
                i++;
                sIndexForMethod++;

                int openBracketNumber = 1, closeBracketNumber = 0;

                while (openBracketNumber>closeBracketNumber) {
                    classMethods[i] = code[sIndexForMethod];
                    if (code[sIndexForMethod] == '{')
                        openBracketNumber++;
                    if (code[sIndexForMethod] == '}') {
                        closeBracketNumber++;
                    }
                        i++;
                        sIndexForMethod++;
                }
        startIndex = sIndexForMethod;
            }
            else
            return classMethods = "";
            }
            else {
                startIndex = firstIndex+className.size();
            }
    }
    return classMethods;
}
/**
 * @brief Метод находит функцию main
 * @return возвращает строку с функцией main
 */
QString Functional::findMainFunc()
{
    QString mainFunction;

    int openBracketNumber = 1, closeBracketNumber = 0, i = 0;
    if (code.indexOf("int main(", 0) >= 0) {
        int firstIndex = code.indexOf("int main(", 0);
        int secondIndex = code.indexOf('{', firstIndex);

        for (; firstIndex <= secondIndex; firstIndex++) {
            mainFunction[i] = code[firstIndex];
            i++;
        }

        while (openBracketNumber > closeBracketNumber) {
            mainFunction[i] = code[firstIndex];
            if (code[firstIndex] == '{')
                openBracketNumber++;
            if (code[firstIndex] == '}') {
                closeBracketNumber++;
            }
                i++;
                firstIndex++;
        }
    }
    return mainFunction;
}

/**
 * @brief Подчищаем за собой
 */
Functional::~Functional()
{
    delete manager;
}
