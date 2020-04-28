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
    int labNumber;
    QString comments;
    QDomElement rootAnswerStructure;

public:
    explicit StrategyLab(QObject* parent = nullptr);
    ~StrategyLab();
    bool check(const QList<QString>);
    bool hasComments() const { return !comments.isEmpty(); }
    QString getComments() const { return comments; }

private:
    bool checkInside(const QList<QString>, const QDomNode&);
    void checkConfig(int variant, QList<QString> *code);
};

#endif // STARTEGYLAB_H
