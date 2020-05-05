#include "testgateway.h"

/**
 * @brief Констркутор класса TestGateway, в котором
 * инициализируется объект тестируемого класса Gateway
 * @param parent
 */
TestGateway::TestGateway(QObject *parent)
    : QObject(parent)
{
    testObj = new Gateway(nullptr);
}

/**
 * @brief Тестовая функция отправляет Gateway полностью корректную строчку формата Json
 */
void TestGateway::testTrueJson()
{
    inputData.append("{\"messageType\": 1, \"lab\": 7, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");

    try {
        testObj->validateData(inputData);
    } catch (WrongRequestException error) {
        qCritical() << error.text();
        QFAIL("Эти тесты должны быть пройдены!");
    }
}
/**
 * @brief Метод, аккумулирующий некорректные Json для далнейшей проверки
 */
void TestGateway::badJsons_data()
{   QTest::addColumn<QByteArray>("jsons");

    QTest::newRow("SendEmpty") << QByteArray("");
    QTest::newRow("SendEmptyJson") << QByteArray("{}");
    QTest::newRow("SendEmptyString") << QByteArray("");
    QTest::newRow("SendSimpleString") << QByteArray("S");
    QTest::newRow("SendWrongLink") << QByteArray("{\"messageType\": 1, \"lab\": 7, \"variant\": 1, \"link\": \"yandex.ru\"}");
    QTest::newRow("SendWrongLabID") << QByteArray("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("SendStringMsgType") << QByteArray("{\"messageType\": \"1\", \"lab\": 7, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("SendWrongMsgType") << QByteArray("{\"messageType\": 3, \"lab\": 7, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("SendWithoutExceptedKey") << QByteArray(" \"lab\": 7, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("SendEveryoneKey") << QByteArray("{\"messageType\": 1, \"lab\": 7, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\", \"code\": 7}");
    QTest::newRow("SendWithExcessKey") << QByteArray("{\"messageType\": 1, \"lab\": 7, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\", \"trpo\": false}");
    QTest::newRow("SendFalseLab") << QByteArray("{\"messageType\": 1, \"lab\": false, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("SendOneKey") << QByteArray("{\"messageType\": 1}");
    QTest::newRow("SendTwoKeys") << QByteArray("{\"messageType\": 1, \"lab\": 7");
    QTest::newRow("SendThreeKeys") << QByteArray("{\"messageType\": 1, \"lab\": 7, \"variant\": 1}");
    QTest::newRow("SendFakeCode") << QByteArray("{\"messageType\": 1, \"lab\": 7, \"variant\": 1, \"code\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("SendFakeVar") << QByteArray("{\"messageType\": 1, \"lab\": 7, \"variant\": 10000, \"link\": \"https://github.com/leshastern/strategy4\"}");
}

/**
 * @brief Тестовая функция извлекает из заранее подготовленной таблицы
 * некорректные Json и отдает их на проверку методу validateData
 */
void TestGateway::badJsons()
{
    QFETCH(QByteArray, jsons);
    try {
      testObj->validateData(jsons);
      QFAIL("Недопустимые данные");
    } catch (WrongRequestException error) {
    }
}

/**
 * @brief Почищаем после всех тестов
 */
void TestGateway::cleanupTestCase()
{
    delete testObj;
}

QTEST_MAIN(TestGateway)
