#include "TestTcp.h"
/**
 * @brief Конструктор класса, в котором создается объект класса QTcpSocket
 * он выполняет фукнцию клиента
 */
TestTcp::TestTcp()
{
    client = new QTcpSocket(this);
    server = new fakeTCP();
};

/**
 * @brief Тестовая функция, которая подключается к серверу
 * @return void
 */
void TestTcp::testConnection()
{
    client ->connectToHost("127.0.0.1", 10000);
    QCOMPARE(client->waitForConnected(1000), true);
};

/**
 * @brief Тестовая функция отправляет строку заданного вида для дальнейшей обработки на сервере
 * @return void
 */
void TestTcp::testSendBadJson()
{
    const char* json = "{\"messageType"": 1, \"lab\": 7, \"variant\": 7, \"link\": \"https://github.com\"}";
    client->write(json);
    QCOMPARE(client->waitForBytesWritten(1000), true);
};

/**
 * @brief Тестовая функция принимает ответ от сервера после всех обработок
 * и сравнивает с ожидаемым результатом
 * @return void
 */
void TestTcp::testGetAnswer()
{
  if (client->waitForReadyRead())
  {
      client->skip(15);
      QByteArray actAnswer = client->readAll();
      QString exAnswer = "\{\n    \"comment\": \"hey\",\n    \"grade\": 1,\n    \"messageType\": 2\n}\n";
      QCOMPARE(actAnswer, exAnswer);
  }
};

void TestTcp::testProcessData()
{
    QString link = "http://github.com";
    QList<QString>* code;
    code->push_back("somecode");
    int variant = 7;
    bool ans = server->FakeProcessData(link,code,variant);
    QCOMPARE(ans, false);

}
/**
 * @brief Тестовая функция выполняет отключение от сервера
 * @return void
 */
void TestTcp::testDisconnection()
{
    client->disconnectFromHost();
    if (client->state() == QAbstractSocket::UnconnectedState
        || client->waitForDisconnected(1000))
    {
            isOff = true;
    }
    QCOMPARE(isOff, true);
};

QTEST_MAIN(TestTcp);
