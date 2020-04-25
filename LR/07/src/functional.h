#ifndef FUNCTIONAL_H
#define FUNCTIONAL_H

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
    bool flag;

public:
    explicit Functional(QObject *parent = nullptr);
    ~Functional();
    void parseIntoClasses(QString, QList<QString>* );

private:
    void getDataFromGithub(QString linkLab);
    void linkChange();

private slots:
    void slotCheckRepo();
};

#endif // FUNCTIONAL_H
