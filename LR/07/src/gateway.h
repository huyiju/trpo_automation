#ifndef GATEWAY_H
#define GATEWAY_H

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
    enum messageType { FROM_CLIENT = 1, DEFAULT_ANSWER, WRONG_REQUEST, SYSTEM_ERROR };

public:
    explicit Gateway(QObject *parent = nullptr);
    QJsonDocument validateData(QByteArray);
    void prepareDataToSend(bool, QString);

private:
    void wrongRequestFormat(QString, QString);

signals:
    void sendToClient(QJsonObject);
    void systemError(QString);

private slots:
    void processSystemError(QString);
};

#endif // GATEWAY_H
