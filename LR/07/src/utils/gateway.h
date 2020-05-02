#ifndef GATEWAY_H
#define GATEWAY_H

#include "internalexception.h"

#include <QDebug>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QDomElement>
#include <QFile>

/**
 * @brief Класс для валидации данных, пришедших с клиента и
 *        формирование ответов сервера
 */
class Gateway : public QObject
{
    Q_OBJECT

private:
    QDomElement rootConfigForClientRequest;
    QDomElement messageKeys;
    QJsonObject jsonObj;
    enum messageType { FROM_CLIENT = 1, DEFAULT_ANSWER, WRONG_REQUEST, SYSTEM_ERROR };

public:
    explicit Gateway(QObject *parent = nullptr);
    QJsonDocument validateData(QByteArray);

    void wrongRequestFormat(QString, QString);
    void processSystemError(QString);
    void prepareDataToSend(bool, QString comments = "");

    void checkKeyExistance();
    void checkKeyTypeAndValue();
    void checkKeyNonExistance();
    void checkMessageType();

signals:
    void sendToClient(QJsonObject);
};

#endif // GATEWAY_H
