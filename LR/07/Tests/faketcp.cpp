#include "faketcp.h"

fakeTCP::fakeTCP()
{
}


bool fakeTCP::FakeProcessData(QString link, QList<QString> *code, int variant)
{
   try {
        if (code->isEmpty()) {
            githubManager->parseIntoClasses(link, code);
        }
        bool result = true;
        QString comments = !result ? lab->getComments() : "";
        emit gateWay->sendCheckResult(result, comments);
        return result;  // окей, все прошло успешно, отправляется дальше на обработку
    } catch (std::exception &e) {
        QString errorMsg = QStringLiteral("Error ' %1 ' while processing data").arg(e.what());
        emit gateWay->systemError(errorMsg);
        qCritical() << errorMsg;
        return false; // произошла ошибка, отправляется соответствующее сообщение клиенту
        }
}
