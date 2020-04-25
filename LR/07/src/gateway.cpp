#include "gateway.h"

/**
 * @brief Читаем конфиги, соединеям сигналы со слотами
 * @param parent
 */
Gateway::Gateway(QObject *parent)
    : QObject(parent)
{
    connect(this, SIGNAL(systemError(QString)), this, SLOT(processSystemError(QString)));
    connect(this, SIGNAL(sendCheckResult(QString)), this, SLOT(prepareDataToSend(QString)));

    // Чтение конфига для валидации запросов клиента
    QDomDocument config;
    QFile file(":/config/jsonSpecificationForClientRequest.xml");
    if (file.open(QIODevice::ReadOnly)) {
        if (config.setContent(&file)) {
            rootConfigForClientRequest = config.documentElement();
        }
        file.close();
    }

    // TODO connect config with reject codes
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
            value = jsonObj.take(key.tagName());
            if (value.isUndefined() && QVariant(key.attribute("required")).toBool()) {
                wrongRequestFormat(keyTagName, QString("Required key does not exist"));
            }

            // Проверка на тип ключа
            if (value.type() != dataTypes.indexOf(key.attribute("type"))) {
                wrongRequestFormat(keyTagName, QString("Wrong key type: '") + key.attribute("type") + QString("' expected"));
            }

            // TODO Проверка на принимаемые значения ключа

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
