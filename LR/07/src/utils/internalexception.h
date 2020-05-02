#ifndef INTERNALEXCEPTION_H
#define INTERNALEXCEPTION_H

#include <QObject>

/**
 * @brief Абстрактный класс обработки исключений
 */
class InternalException
{

private:
    QString errorMessage;

public:
    InternalException(QString explanation, QString systemMessage = "")
    {
        formatMessage(explanation, systemMessage);
    }

    virtual ~InternalException() {}

    virtual const QString text()
    {
        return errorMessage;
    }

private:
    void formatMessage(QString, QString);
};

class SystemException : public InternalException
{
public:
    SystemException(QString explanation, QString systemMessage = "")
        : InternalException(explanation, systemMessage)
    {}

    ~SystemException() {}
};

class UnexpectedResultException : public InternalException
{
public:
    UnexpectedResultException(QString explanation, QString systemMessage = "")
        : InternalException(explanation, systemMessage)
    {}

    ~UnexpectedResultException() {}
};

#endif // INTERNALEXCEPTION_H
