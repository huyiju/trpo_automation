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
    lab = new StrategyLab();
    github = new Functional();

    connect(gateWay, SIGNAL(sendToClient(QJsonObject)), this, SLOT(slotSendToClient(QJsonObject)));
    connect(mTcpServer, &QTcpServer::newConnection, this, &TcpServer::slotNewConnection);

    if (!mTcpServer->listen(QHostAddress::LocalHost, 12345)) {
        qDebug() << mTcpServer->errorString();
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

    connect(mTcpSocket, SIGNAL(readyRead()), this, SLOT(slotReadingDataJson()));
    connect(mTcpSocket, &QTcpSocket::disconnected, this, &TcpServer::slotClientDisconnected);

    mTcpSocket->write("New connection!");
}

/**
 * @brief Метод выключает сервер.
 * @return void
 */
void TcpServer::slotClientDisconnected()
{
    mTcpSocket->close();
}

/**
 * @brief Метод отправляет клиенту строку в формате json
 * @param QJsonObjecr answerJson - ответ для клиента
 * @return void
 */
void TcpServer::slotSendToClient(QJsonObject answerJson)
{
    QJsonDocument jsonDoc(answerJson);
    QString jsonString = QString::fromLatin1(jsonDoc.toJson());

    mTcpSocket->readAll();
    mTcpSocket->write(jsonString.toLatin1());
}

/**
 * @brief Метод получает данные от клиента в формате json и отдает их на обработку
 * @return void
 */
void TcpServer::slotReadingDataJson()
{
    QByteArray data;
    QString labLink;
    QList<QString> pureCode;
    int labNumber = 1;

    data = mTcpSocket->readAll();

    try {
        QJsonDocument jsonDoc = gateWay->validateData(data);
        if (!jsonDoc.isNull()) {
            parsingJson(jsonDoc, &labLink, &labNumber, &pureCode);
            processData(labLink, &pureCode, labNumber);
        }
    } catch (SystemException error) {
        emit gateWay->systemError(QString("Error ' %1 ' while processing data").arg(error.text()));
    }
}

/**
 * @brief Метод парсинга пришедших с почтового сервиса Json-данных
 * @param docJson - объект json
 * @param labLink - ссылка на репозиторий решения на Github
 * @param labNumber - номер лабы
 * @param pureData - массив строчек (каждая строчка - класс решения с телами методов)
 */
void TcpServer::parsingJson(QJsonDocument docJson, QString *labLink, int *labNumber, QList<QString> *pureData)
{
    QJsonValue link;
    QJsonObject jsonObj;

    jsonObj = docJson.object();

    link = jsonObj.take("link");
    if (!link.isUndefined()) {
        (*labLink) = link.toString();
    } else {
        link = jsonObj.take("code");
        foreach (QJsonValue item, link.toArray()) {
            (*pureData).append(item.toString());
        }
    }

    link = jsonObj.take("variant");
    (*labNumber) = link.toInt();
}

/**
 * @brief (коммент года!)Метод обрабатывает код решения пришедший от клиента, проверяет на правильность
 *        и оставляет комментарии, если они необходимы. После этого передает данные для подготовки их передаче клиенту
 * @param link - ссылка на Github репозиторий решения
 * @param code - распарсенный код в массив строчек
 * @param variant - вариант лабы
 */
void TcpServer::processData(QString link, QList<QString> *code, int variant)
{
    try {
        if (code->isEmpty()) {
            QUrl urlForRequest = github->linkChange(link);
            QString fileName;
            github->getRequest(urlForRequest, [this, &fileName](QJsonDocument reply) {
                github->getFileInside(reply.array(), fileName);
            });

            if (fileName.isEmpty()) {
                throw UnexpectedResultException(QString("You don't have file with .cpp extension inside your repo"));
            }

            github->getRequest(QUrl(urlForRequest.toString() + "/" + fileName),
                               [this, code](QJsonDocument reply) {
                github->parseIntoClasses(github->getCode(reply), code);
            });
        }

        bool result = lab->check(variant, *code);
        QString comments = !result ? lab->getComments() : "";

        gateWay->sendCheckResult(result, comments);
    } catch (UnexpectedResultException error) {
        gateWay->sendCheckResult(false, QString("Error ' %1 ' while checking the lab").arg(error.text()));
    } catch (SystemException error) {
        throw error;
    }
}

/**
 * @brief Деструктор
 */
TcpServer::~TcpServer()
{
    delete mTcpServer;
    delete gateWay;
    delete lab;
    delete github;
}
