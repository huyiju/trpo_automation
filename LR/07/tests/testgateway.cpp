#include "testgateway.h"

TestGateway::TestGateway(QObject *parent)
    : QObject(parent)
{}

void TestGateway::shouldWork()
{
    QString str = "Hello";
    QCOMPARE(str.toUpper(), QString("HELLO"));
}

QTEST_MAIN(TestGateway)
