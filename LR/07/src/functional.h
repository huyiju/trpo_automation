#ifndef FUNCTIONAL_H
#define FUNCTIONAL_H

#include "gateway.h"

#include <QObject>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>

/**
 * @brief Класс для получения листинга кода с GitHub
 */
class Functional : public QObject
{
    Q_OBJECT

public:
    QNetworkReply *reply;

private:
    QNetworkAccessManager *manager;
    QString link;
    QString code;
    bool flag;

public:
    explicit Functional(QObject *parent = nullptr);
    ~Functional();
    void parseIntoClasses(QString linkLab, QList<QString>* );

private:
    QString findMainFunc();
    QString findNameOfClass(int);
    QString findClassMethods(QString, int);
    void linkChange();
    void getCode(QNetworkReply *reply);
    void getDataFromGithub(QString linkLab);

private slots:
    void slotCheckRepo();
};

#endif // FUNCTIONAL_H
