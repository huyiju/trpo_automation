#include "testgateway.h"

/**
 * @brief Констркутор
 * @param parent
 */
TestGateway::TestGateway(QObject *parent)
    : QObject(parent)
{
    testObj = new Gateway(nullptr);
}
/**
 * @brief Тестовая функция отправляет Gateway полностью корректный Json
 */
void TestGateway::testTrueData()
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
 * @brief Тестовая функция осуществляет серию проверок с некорректным вводом
 */
void TestGateway::badData()
{   QTest::addColumn<QByteArray>("jsons");

    QTest::newRow("s1") << QByteArray("S");
   /** QTest::newRow("11") << inputData.append("{\"messageType\": 1, \"lab\": 7, \"variant\": 1, \"link\": \"yandex.ru\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": \"1\", \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QTest::newRow("12") << inputData.append("{\"messageType\": 1, \"lab\": 8, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    */

}
void TestGateway::testBadData()
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
