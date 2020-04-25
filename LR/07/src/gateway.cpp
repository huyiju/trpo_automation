#include "gateway.h"

/**
 * @brief Читаем конфиги, соединеям сигналы со слотами
 * @param parent
 */
Gateway::Gateway(QObject *parent)
    : QObject(parent)
{
    connect(this, SIGNAL(systemError(QString)), this, SLOT(processSystemError(QString)));

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
    QJsonObject jsonObj;
    QJsonValue value;
    QJsonDocument jsonData = QJsonDocument::fromJson(data, &docJsonError);
    const QList<QString> dataTypes({"Null", "Bool", "Double", "String", "Array", "Object"});

    if (docJsonError.error == QJsonParseError::NoError) {
        for (QDomElement key = rootConfigForClientRequest.firstChild().toElement();
             !key.isNull(); key = key.nextSibling().toElement())
        {
            jsonObj = jsonData.object();
            QString keyTagName = key.tagName();

            // Проверка на наличие нужного ключа
            value = jsonObj.take(keyTagName);
            if (value.isUndefined() && QVariant(key.attribute("required")).toBool()) {
                wrongRequestFormat(keyTagName, QString("Required key does not exist"));
            }

            // Проверка на тип ключа
            QString keyType = key.attribute("type");
            if (value.type() != dataTypes.indexOf(keyType)) {
                wrongRequestFormat(keyTagName, QString("Wrong key type: '") + keyType + QString("' expected"));
            }

            // Проверка на принимаемые значения ключа
            QVariant jsonValue = value.toVariant();
            if (key.hasAttribute("range") && QVariant(key.attribute("range")).toBool()) {

                // Пока только для чисел
                if (keyType == "Double") {
                    int startValue = key.firstChildElement().attribute("value").toInt();
                    int endValue = key.lastChildElement().attribute("value").toInt();

                    if (!(startValue <= jsonValue.toInt() && jsonValue.toInt() <= endValue)) {
                        wrongRequestFormat(keyTagName, QString("Wrong value: from ") + \
                                           QString(startValue) + " to " +  QString(endValue) + QString(" expected"));
                    }
                }
            }

            if (key.hasAttribute("severalChecks") && \
                    QVariant(key.attribute("severalChecks")).toBool()) {

                // Пока только для строк
                if (keyType == "String") {
                    for (QDomElement check = key.firstChild().toElement();
                         !check.isNull(); check = check.nextSibling().toElement()) {

                        QRegExp re(check.attribute("value"));
                        if (!re.exactMatch(jsonValue.toString())) {
                            wrongRequestFormat(keyTagName, QString("Wrong value: it should match regex ") + check.attribute("value"));
                        }
                    }
                }
            }

            if (key.hasAttribute("value")) {
                if (QVariant(key.attribute("value")) != jsonValue) {
                    wrongRequestFormat(keyTagName, QString("Wrong value: they just don't match"));
                }
            }
        }

        // TODO Проверка на отсутствие ключей, которых нет в спецификации
    } else {
        wrongRequestFormat(QString(""), QString("Wrong json object: ") + docJsonError.errorString());
    }

    return jsonData;
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
    throw QString("Client - ") + text;
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
    throw QString("Internal - ") + errorMsg;
}
