#ifndef STARTEGYLAB_H
#define STARTEGYLAB_H

#include "utils/internalexception.h"

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
    QDomElement rootAnswerStructure;
    QMap<QString, QString> classes;
    QList<QString> children;
    QString abstractClassName;
    QString abstractMethodName;
    int heirsAmount;

public:
    explicit StrategyLab(QObject* parent = nullptr);
    ~StrategyLab();
    void checkByConfig(int, QList<QString>);
    void checkParentChildrenRelations();
    void checkContext();
    void checkMainFunction();

private:
    void checkAbstractMethodModifier(QString, QString, QString modifier = "public");
    void checkChildren();
};

#endif // STARTEGYLAB_H
