#include "testgateway.h"

TestGateway::TestGateway(QObject *parent)
    : QObject(parent)
{}

void TestGateway::initTestCase()
{
    testObj = new Gateway(nullptr);
}

void TestGateway::cleanupTestCase()
{
    delete testObj;
}

void TestGateway::cleanup()
{
    inputData.clear();
}

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

void TestGateway::requiredKeyDoesNotExist()
{
    inputData.append("{\"lab\": 7, \"variant\": 1, \"link\": \"https://github.com/leshastern/strategy4\"}");
    QVERIFY_EXCEPTION_THROWN(testObj->validateData(inputData), WrongRequestException);
}

QTEST_MAIN(TestGateway)
