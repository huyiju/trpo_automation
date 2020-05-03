#ifndef INTERNALEXCEPTION_H
#define INTERNALEXCEPTION_H

#include <QObject>

/**
 * @brief Абстрактный класс обработки исключений
 */
class InternalException
{

protected:
    QString errorMessage;

protected:
    InternalException(QString explanation, QString systemMessage = "")
    {
        formatMessage(explanation, systemMessage);
    }

    virtual ~InternalException() {}
    virtual void formatMessage(QString, QString);

public:
    const QString text()
    {
        return errorMessage;
    }
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

class WrongRequestException : public InternalException
{
private:
    QString key;

public:
    WrongRequestException(QString key, QString explanation, QString systemMessage = "")
        : InternalException(explanation, systemMessage),
          key(key)
    {}

    ~WrongRequestException() {}

    const QString jsonKey()
    {
        return key;
    }
};


#endif // INTERNALEXCEPTION_H
