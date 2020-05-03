#ifndef TESTGATEWAY_H
#define TESTGATEWAY_H

#include "../src/utils/gateway.h"

#include <QObject>
#include <QtTest/QtTest>

class TestGateway : public QObject
{
    Q_OBJECT
public:
    explicit TestGateway(QObject *parent = nullptr);

private slots:
    void shouldWork();
};

#endif // TESTGATEWAY_H
