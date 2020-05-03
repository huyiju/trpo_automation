#ifndef FUNCTIONAL_H
#define FUNCTIONAL_H

#include "utils/gateway.h"
#include "utils/internalexception.h"

#include <QObject>
#include <QtGlobal>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QEventLoop>
#include <QFileInfo>

static const QString GITHUB_URL("https://api.github.com");
static const QString USER_AGENT("GitHubPP");
static const QString FILE_EXTENSION("cpp");

/**
 * @brief Класс для получения листинга кода с GitHub
 */
class Functional : public QObject
{
    Q_OBJECT

private:
    QNetworkAccessManager *manager;
    QList<QString>* ListOfClasses;
    QString code;

public:
    explicit Functional(QObject *parent = nullptr);
    ~Functional();
    void getRequest(QUrl, const std::function<void(QJsonDocument)> &);
    void getFileInside(QJsonArray, QString&);
    void parseIntoClasses(QString linkLab, QList<QString>* );
    QUrl linkChange(QString&);
    QString getCode(QJsonDocument);

private:
    QString findMainFunc();
    QString findNameOfClass(int);
    QString findClassMethods(QString, int);

    QJsonDocument handleReply(QNetworkReply*);
};

#endif // FUNCTIONAL_H
