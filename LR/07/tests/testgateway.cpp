#include "testgateway.h"

/**
 * @brief Констркутор
 * @param parent
 */
TestGateway::TestGateway(QObject *parent)
    : QObject(parent)
{}

/**
 * @brief Выполняем перед всеми тестами
 */
void TestGateway::initTestCase()
{
    testObj = new Gateway(nullptr);
}

/**
 * @brief Почищаем после всех тестов
 */
void TestGateway::cleanupTestCase()
{
    delete testObj;
}

/**
 * @brief подчищаем после каждого теста
 */
void TestGateway::cleanup()
{
    inputData.clear();
}

/**
 * @brief Положительный тест
 */
void TestGateway::validateSuccessful()
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
 * @brief Отрицательный тест: отсутствует необходимый ключ
 */
void TestGateway::requiredKeyDoesNotExist()
{
    inputData.append("{\"lab\": 7, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");

    try {
        testObj->validateData(inputData);
        QFAIL("Нет обязательного ключа, не выбросил исключение");
    } catch (WrongRequestException error) {
//        qCritical() << error.text();
    }
//    QVERIFY_EXCEPTION_THROW(testObj->validateData(inputData), WrongRequestException);
}

QTEST_MAIN(TestGateway)
