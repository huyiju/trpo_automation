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
    bool checkParentChildrenRelations(int);
    bool checkContext();
    bool checkMainFunction();

    bool checkAbstractMethodModifier(QString, QString, QString, QString modifier = "public");
    bool checkParent(QString, QString, QString);
    bool checkChildren(QList<QString>, QString, QString, int);
};

#endif // STARTEGYLAB_H
