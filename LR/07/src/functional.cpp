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
               // TODO Убрать к чертям, когда придумаем свой Exception
               Gateway *tmp = new Gateway;
               emit tmp->sendCheckResult(false, message);
               delete tmp;
         }

            /* Получаем данные файла */
            flag = false;
            getDataFromGithub(link);

        } else {

            /* Извлекаем код программы из Json объекта */
            getCode(reply);
        }
    } else {
        message = reply->errorString();
        // TODO Убрать к чертям, когда придумаем свой Exception
        Gateway *tmp = new Gateway;
        emit tmp->sendCheckResult(false, message);
        delete tmp;
    }
}

/**
 * @brief Метод извлекает код программы из Json
 * @param reply - Json, который присылает GitHub
 * @return void
 */
void Functional::getCode(QNetworkReply *reply)
{
    QString tempString;
    QByteArray jsonData;
    QJsonObject object;

    jsonData = reply->readAll();

    object = QJsonDocument::fromJson(jsonData).object();
    tempString = object.take("content").toString();

    jsonData.clear();
    jsonData.append(tempString);
    tempString = jsonData.fromBase64(jsonData).data();
    code = tempString;
}
/**
 * @brief Метод разделяет полученный код на классы
 *        и помещает их в массив
 * @return void
 */
void Functional::parseIntoClasses(QString link, QList<QString>* ListOfClasses)
{
    getDataFromGithub(link);
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
    while (code[firstIndex] == " ") {
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

        qDebug() << firstIndex;
        qDebug() << secondIndex;

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
