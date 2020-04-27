#ifndef FAKETCP_H
#define FAKETCP_H
#include "../src/tcpserver.h"
class fakeTCP : public TcpServer
{
public:
    fakeTCP();
    StrategyLab* lab;
    Functional* githubManager;
    Gateway* gateWay;
    bool FakeProcessData(QString, QList<QString>*, int);
};

#endif // FAKETCP_H
