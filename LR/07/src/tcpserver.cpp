#include "tcpserver.h"

/**
 * @brief Конструктор класса, в котором создается объект класса QTcpServer
 * Сервер включается и ждет новых соединений.
 */
TcpServer::TcpServer(QObject *parent)
        : QObject(parent)
{
    mTcpServer = new QTcpServer(this);
    gateWay = new Gateway();

    connect(gateWay, SIGNAL(sendToClient(QJsonObject)), this, SLOT(sendToClient(QJsonObject)));
    connect(mTcpServer, &QTcpServer::newConnection, this, &TcpServer::slotNewConnection);

    if (!mTcpServer->listen(QHostAddress::LocalHost, 10000)) {
        qDebug() << "Server is not started";
    } else {
        qDebug() << "Server is started";
    }
}

/**
 * @brief Метод отвечающий за подключение клиента к серверу
 * @return void
 */
void TcpServer::slotNewConnection()
{
    mTcpSocket = mTcpServer->nextPendingConnection();

    mTcpSocket->write("New connection!");

    connect(mTcpSocket, &QTcpSocket::readyRead, this, &TcpServer::slotReadingDataJson);
    connect(mTcpSocket, &QTcpSocket::disconnected, this, &TcpServer::slotClientDisconnected);
}

/**
 * @brief метод выключает сервер.
 * @return void
 */
void TcpServer::slotClientDisconnected()
{
    mTcpSocket->close();
}

/**
 * @brief Метод отправляет клиенту строку в формате
 * @param unsigned char grade - оценка за лабораторную работу
 * @param QString comment - описание системной ошибки, либо комментарий сдающему лабораторную
 * @return void
 */
void TcpServer::sendToClient(unsigned char grade, QString comment)
{
    const unsigned char MESSAGE_TYPE = 2;
    QJsonObject json;

    json ["messageType"] = MESSAGE_TYPE;
    json ["grade"] = grade;

    if (comment != NULL) {
        json ["comment"] = comment;
    }

    QJsonDocument jsonDoc(json);
    QString jsonString = QString::fromLatin1(jsonDoc.toJson());

    mTcpSocket->readAll();
    mTcpSocket->write(jsonString.toLatin1());
}

/**
 * @brief Метод получает данные от клиента в формате json
 * @return void
 */
void TcpServer::slotReadingDataJson()
{
    QByteArray data;
    QString labLink, mistakeDescription;
    QList<QString> pureCode;
    bool grade = false, errorSystem = true;
    int labNumber = 1;

    if (mTcpSocket->waitForConnected(500)) {
        mTcpSocket->waitForConnected(500);
        data = mTcpSocket->readAll();

        try {
            QJsonDocument docJson = gateWay->validateData(data);
            if (parsingJson(docJson, &labLink, &labNumber, &pureCode)) {
                githubManager = new Functional(labLink);
            }

            lab = new StrategyLab(labNumber);
            grade = lab->check(pureCode);
            if (lab->hasComments()) {
                errorSystem = false;
                qDebug() << lab->getComments();
                mistakeDescription += "\n\nОшибки в решении:\n" + lab->getComments();
            }
        } catch (QString errorMsg) {
            qCritical() << errorMsg;
        }

        delete lab;
        delete githubManager;
    }
}

/**
 * @brief Метод парсинга пришедших с почтового сервиса Json-данных
 * @param docJson - объект json
 * @param labLink - ссылка на репозиторий решения на Github
 * @param labNumber - номер лабы
 * @param pureData - массив строчек (каждая строчка - класс решения с телами методов)
 * @return bool - Если в поле data пришла ссылка на репозиторий Github - то true, иначе false
 */
bool TcpServer::parsingJson(QJsonDocument docJson, QString *labLink, int *labNumber, QList<QString> *pureData)
{
    QJsonValue link;
    QJsonObject jsonObj;
    bool needToAccessGithub = true;

    jsonObj = docJson.object();

    link = jsonObj.take("link");
    if (!link.isUndefined()) {
        (*labLink) = link.toString();
    } else {
        needToAccessGithub = false;
        link = jsonObj.take("code");
        foreach (QJsonValue item, link.toArray()) {
            (*pureData).append(item.toString());
        }
    }

    link = jsonObj.take("variant");
    (*labNumber) = link.toInt();

    return needToAccessGithub;
}

/**
 * @brief TcpServer::processData
 * @param link - ссылка на Github репозиторий решения
 * @param code - распарсенный код в массив строчек
 */
void TcpServer::processData(QString link, QList<QString> *code, int variant)
{
    if (code->isEmpty()) {
        githubManager->parseIntoClasses(link, code);
    }

    bool result = lab->check(variant, code);
    QString comments = !result ? lab->getComments() : "";

    try {
        delete lab;
        delete githubManager;
        Gateway::prepareDataToSend(result, comments);
    } catch (std::exception &e) {
        QString errorMsg = QStringLiteral("Error %1 while preparing check-data for sending").arg(e.what());
        emit gateWay->systemError(errorMsg);
        qCritical() << errorMsg;
    }
}
