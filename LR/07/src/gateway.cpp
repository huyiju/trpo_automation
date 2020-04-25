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
    QJsonDocument jsonData = QJsonDocument::fromJson(data, &docJsonError);
    jsonObj = jsonData.object();

    if (docJsonError.error == QJsonParseError::NoError) {
        checkKeyExistance();
        checkKeyTypeAndValue();
        checkKeyNonExistance();
    } else {
        wrongRequestFormat(QString(""), QString("Wrong json object: ") + docJsonError.errorString());
    }

    return jsonData;
}

/**
 * @brief Проверка на то, что в сообщении сожержаться необходимые ключи
 */
void Gateway::checkKeyExistance()
{
    QJsonValue value;
    QMap<QString, QString> dependKeys = {};

    for (QDomElement key = rootConfigForClientRequest.firstChildElement();
         !key.isNull(); key = key.nextSibling().toElement())
    {
        QString keyTagName = key.tagName();

        value = jsonObj.take(keyTagName);
        if (key.hasAttribute("required")) {
            if (value.isUndefined() && QVariant(key.attribute("required")).toBool()) {
                wrongRequestFormat(keyTagName, QString("Required key does not exist"));
            }
        } else {
            dependKeys.insert(keyTagName, key.attribute("dependsOn"));
        }
    }

    foreach (QString key, dependKeys.keys()) {
        QString pairKey = dependKeys.value(key);
        bool gotFirstKey = !jsonObj.take(key).isUndefined();
        bool gotSecondKey = !jsonObj.take(pairKey).isUndefined();

        if ((gotFirstKey && gotSecondKey) || \
                (!gotFirstKey && !gotSecondKey)) {

            QString errKey = gotFirstKey ? pairKey : key;
            wrongRequestFormat(errKey, QString("Key ") + \
                (gotFirstKey \
                    ? "exists but should not, because key '" + dependKeys.value(errKey) + "' exists" \
                    : "does not exist but should, because key '" + dependKeys.value(errKey) + "' does not exits")
            );
        }
    }
}

/**
 * @brief Проверки на тип ключа и на допустимые принимаемые значения
 */
void Gateway::checkKeyTypeAndValue()
{
    const QList<QString> dataTypes({"Null", "Bool", "Double", "String", "Array", "Object"});
    QJsonValue value;

    for (QDomElement key = rootConfigForClientRequest.firstChildElement();
         !key.isNull(); key = key.nextSibling().toElement())
    {
        QString keyTagName = key.tagName();
        value = jsonObj.take(keyTagName);

        // Проверка на тип ключа
        QString keyType = key.attribute("type");
        if (value.type() != dataTypes.indexOf(keyType)) {
            wrongRequestFormat(keyTagName, QString("Wrong key type: '") + keyType + QString("' expected"));
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
                                       QString(startValue) + " to " +  QString(endValue) + QString(" expected"));
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
                    }
                }
            }
        } else if (key.hasAttribute("value")) {

            // Проверка на полное соответствие
            if (QVariant(key.attribute("value")) != jsonValue) {
                wrongRequestFormat(keyTagName, QString("Wrong value: they just don't match"));
            }
        }
    }
}

/**
 * @brief Проверяем, что в запросе не пришел неожиданный ключ
 */
void Gateway::checkKeyNonExistance()
{
    QJsonValue value;
    foreach (const QString& key, jsonObj.keys()) {
        if (rootConfigForClientRequest.elementsByTagName(QString(key)).isEmpty()) {
            wrongRequestFormat(key, QString("Unexpected key"));
        }
    }
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
