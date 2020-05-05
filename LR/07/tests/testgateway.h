#ifndef TESTGATEWAY_H
#define TESTGATEWAY_H

#include "../src/utils/gateway.h"
#include "../src/utils/internalexception.h"

#include <QObject>
#include <QtTest/QtTest>

/**
 * @brief Класс тестирования сервиса Gateway
 */
class TestGateway : public QObject
{
    Q_OBJECT

private:
    Gateway *testObj;
    QByteArray inputData;

public:
    explicit TestGateway(QObject *parent = nullptr);

private slots:
    void testTrueJson();
    void badJsons_data();
    void badJsons();
    void cleanupTestCase();
};

#endif // TESTGATEWAY_H
