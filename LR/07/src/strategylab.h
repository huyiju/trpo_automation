#ifndef STARTEGYLAB_H
#define STARTEGYLAB_H

#include <QObject>
#include <QtXml>

/**
 * @brief Класс для проверки лабораторных работ
 *  по паттерну 'Стратегия'
 */
class StrategyLab: public QObject
{
    Q_OBJECT

private:
    int variant;
    QString comments;
    QDomElement rootAnswerStructure;
    QMap<QString, QString> classes;

public:
    explicit StrategyLab(QObject* parent = nullptr);
    ~StrategyLab();
    bool check(int, QList<QString>*);
    bool hasComments() const { return !comments.isEmpty(); }
    QString getComments() const { return comments; }

private:
    bool checkByConfig(int, QList<QString>*);
    bool checkParentChildRelations(int);
    bool checkContext();
    bool checkMainFunction();


};

#endif // STARTEGYLAB_H
