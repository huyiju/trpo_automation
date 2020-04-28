#include "gateway.h"

/**
 * @brief Читаем конфиги, соединеям сигналы со слотами
 * @param parent
 */
Gateway::Gateway(QObject *parent)
    : QObject(parent)
{
    connect(this, SIGNAL(systemError(QString)), this, SLOT(processSystemError(QString)));
    connect(this, SIGNAL(sendCheckResult(bool, QString)), this, SLOT(prepareDataToSend(bool, QString)));

    // Чтение конфига для валидации запросов клиента
    QDomDocument config;
    QFile file(":/config/jsonSpecificationForClientRequest.xml");
    if (file.open(QIODevice::ReadOnly)) {
        if (config.setContent(&file)) {
            rootConfigForClientRequest = config.documentElement();
        }
        file.close();
    }
}

/**
 * @brief Метод валидации данных, с клиента
 * @param data - сырые данные с клиента
 * @return
 */
QJsonDocument Gateway::validateData(QByteArray data)
{
    QJsonParseError docJsonError;
    QJsonDocument jsonDoc = QJsonDocument::fromJson(data, &docJsonError);
    QJsonDocument *empty = new QJsonDocument();

    if (docJsonError.error == QJsonParseError::NoError) {
        jsonObj = jsonDoc.object();

        // Сначала проверим messageType - костыль - TODO выпилить
        QDomElement elem = rootConfigForClientRequest.firstChildElement();
        QJsonValue messageType = jsonObj.value(elem.tagName());
        const int expectedType = 2;

        if (messageType.isUndefined()) {
            wrongRequestFormat(QString(elem.tagName()), QString("Required key does not exist, cancel processing..."));
            return (*empty);
        }

        if (messageType.type() != expectedType) {
            wrongRequestFormat(QString(elem.tagName()), QString("Key should have different type, cancel processing..."));
            return (*empty);
        }

        if (messageType.toInt() != elem.attribute("value").toInt()) {
            wrongRequestFormat(QString(elem.tagName()), QString("Key should have different value, cancel processing..."));
            return (*empty);
        }


        if (!checkKeyExistance()
                || !checkKeyTypeAndValue()
                || !checkKeyNonExistance()) {
            return (*empty);
        }
    } else {
        wrongRequestFormat(QString(""), QString("Wrong json object: system says - '") + docJsonError.errorString() + "'");
        return (*empty);
    }

    return jsonDoc;
}

/**
 * @brief Проверка на то, что в сообщении сожержаться необходимые ключи
 */
bool Gateway::checkKeyExistance()
{
    QJsonValue value;
    QMap<QString, QString> dependKeys = {};

    for (QDomElement key = rootConfigForClientRequest.firstChildElement();
         !key.isNull(); key = key.nextSibling().toElement())
    {
        QString keyTagName = key.tagName();

        value = jsonObj.value(keyTagName);
        if (key.hasAttribute("required")) {
            if (value.isUndefined() && QVariant(key.attribute("required")).toBool()) {
                wrongRequestFormat(keyTagName, QString("Required key does not exist"));
                return false;
            }
        } else {
            dependKeys.insert(keyTagName, key.attribute("dependsOn"));
        }
    }

    foreach (QString key, dependKeys.keys()) {
        QString pairKey = dependKeys.value(key);
        bool gotFirstKey = !jsonObj.value(key).isUndefined();
        bool gotSecondKey = !jsonObj.value(pairKey).isUndefined();

        if ((gotFirstKey && gotSecondKey) || \
                (!gotFirstKey && !gotSecondKey)) {

            QString errKey = gotFirstKey ? pairKey : key;
            wrongRequestFormat(errKey, QString("Key '" + errKey + "' or key '" + dependKeys.value(errKey) + "' should exist"));
            return false;
        }
    }

    return true;
}

/**
 * @brief Проверки на тип ключа и на допустимые принимаемые значения
 */
bool Gateway::checkKeyTypeAndValue()
{
    const QList<QString> dataTypes({"Null", "Bool", "Double", "String", "Array", "Object"});
    QJsonValue value;

    for (QDomElement key = rootConfigForClientRequest.firstChildElement();
         !key.isNull(); key = key.nextSibling().toElement())
    {
        QString keyTagName = key.tagName();
        value = jsonObj.value(keyTagName);

        // TODO - выпилить - костыль
        if (!value.isUndefined()) {

            // Проверка на тип ключа
            QString keyType = key.attribute("type");
            if (value.type() != dataTypes.indexOf(keyType)) {
                wrongRequestFormat(keyTagName, QString("Wrong key type: '") + keyType + QString("' expected"));
                return false;
            }

            /*** Проверки на принимаемые значения ключа ***/

            QVariant jsonValue = value.toVariant();
            if (key.hasAttribute("range") && QVariant(key.attribute("range")).toBool()) {

                // Значение попадает в заданный интервал - пока только для чисел
                if (keyType == "Double") {
                    int startValue = key.firstChildElement().attribute("value").toInt();
                    int endValue = key.lastChildElement().attribute("value").toInt();

                    if (!(startValue <= jsonValue.toInt() && jsonValue.toInt() <= endValue)) {
                        wrongRequestFormat(keyTagName, QString("Wrong value: from ") + \
                                           QString::number(startValue) + " to " +  QString::number(endValue) + QString(" expected"));
                        return false;
                    }
                }
            } else if (key.hasAttribute("severalChecks") && \
                    QVariant(key.attribute("severalChecks")).toBool()) {

                // Значение удовлетворяет всем проверкам - пока только набор регулярок для строк
                if (keyType == "String") {
                    for (QDomElement check = key.firstChildElement();
                         !check.isNull(); check = check.nextSibling().toElement()) {

                        QRegExp re(check.attribute("value"));
                        if (!re.exactMatch(jsonValue.toString())) {
                            wrongRequestFormat(keyTagName, QString("Wrong value: it should match regex ") + check.attribute("value"));
                            return false;
                        }
                    }
                }
            } else if (key.hasAttribute("value")) {

                // Проверка на полное соответствие
                if (QVariant(key.attribute("value")) != jsonValue) {
                    wrongRequestFormat(keyTagName, QString("Wrong value: they just don't match"));
                    return false;
                }
            }
        }
    }

    return true;
}

/**
 * @brief Проверяем, что в запросе не пришел неожиданный ключ
 */
bool Gateway::checkKeyNonExistance()
{
    QJsonValue value;
    foreach (const QString& key, jsonObj.keys()) {
        if (rootConfigForClientRequest.elementsByTagName(QString(key)).isEmpty()) {
            wrongRequestFormat(key, QString("Unexpected key"));
            return false;
        }
    }

    return true;
}

/**
 * @brief Слот формирования json-ответа при неверном формате запроса клиента
 * @param jsonKey - ключ, где обнаружена ошибка
 * @param text - текст ошибки
 */
void Gateway::wrongRequestFormat(QString jsonKey, QString text)
{
    QJsonObject jsonObj {
        {"messageType", messageType::WRONG_REQUEST},
        {"key", jsonKey},
        {"text", text}
    };

    emit sendToClient(jsonObj);
    qCritical() << QString("Client - ") + text;
}

/**
 * @brief Слот формирования json-ответа при возникновении системной ошибки на сервере
 * @param errorMsg - текст ошибки
 */
void Gateway::processSystemError(QString errorMsg)
{
    QJsonObject jsonObj {
        {"messageType", messageType::SYSTEM_ERROR},
        {"errorMessage", errorMsg}
    };

    emit sendToClient(jsonObj);
    qCritical() << QString("Internal - ") + errorMsg;
}

/**
 * @brief Метод формирования ответа клиенту о проверенной лабе
 * @param grade - оценка за работу
 * @param comments - комментарии к работе
 */
void Gateway::prepareDataToSend(bool grade, QString comments)
{
    QJsonObject jsonObj {
        {"messageType", messageType::DEFAULT_ANSWER},
        {"grade", int(grade)}
    };

    if (!grade && !comments.isEmpty()) {
        jsonObj.insert("comment", comments);
    }

    emit sendToClient(jsonObj);
}
