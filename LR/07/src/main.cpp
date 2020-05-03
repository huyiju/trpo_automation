#include <QCoreApplication>
#include "tcpserver.h"

static const int LAB_NUMBER = 7;

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    TcpServer* server = new TcpServer(LAB_NUMBER);

    return a.exec();
}
