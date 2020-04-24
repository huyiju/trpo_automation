#ifndef FUNCTIONAL_H
#define FUNCTIONAL_H

#include <QObject>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QJsonDocument>
#include <QJsonObject>

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

public:
    explicit Functional(QString linkLab, QObject *parent = nullptr);
    ~Functional();
    void getDataFromGithub();
    void dataProcessing();

private:
    void linkChange();

private slots:
    void slotCheckRepo();
};

#endif // FUNCTIONAL_H
