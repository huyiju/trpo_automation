#ifndef TCPSERVER_H
#define TCPSERVER_H

#include "strategylab.h"
#include "functional.h"
#include "gateway.h"

#include <QTcpServer>
#include <QTcpSocket>
#include <QJsonDocument>
#include <QJsonObject>

/**
*   @brief Реализация сервера для проверки лабораторных работ по паттерну стратегии
*/
class TcpServer : public QObject
{
    Q_OBJECT

private:
    QTcpServer* mTcpServer;
    QTcpSocket* mTcpSocket;
    StrategyLab* lab;
    Functional* githubManager;
    Gateway* gateWay;
    QJsonDocument docJson;
    QJsonParseError docJsonError;

public:
    explicit TcpServer(QObject *parent = nullptr);
    ~TcpServer();
    void processData(QString, QList<QString>*, int);
    
private:
    void parsingJson(QJsonDocument, QString*, int*, QList<QString>*);

public slots:
    void slotNewConnection();
    void slotClientDisconnected();
    void slotReadingDataJson();
    void slotSendToClient(QJsonObject answerJson);

};

#endif // TCPSERVER_H
