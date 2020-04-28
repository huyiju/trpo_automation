#include "strategylab.h"

/**
 * @brief Конструктор
 * @param objectFromServer
 * @param parent
 */
StrategyLab::StrategyLab(QObject* parent)
    : QObject(parent)
{
    /* Подключаем answerStructure.xml для проверки лабораторной работы
       Храниться в rootAnswerStructure */
    QDomDocument config;
    QFile file(":/config/answerStructure.xml");
    if (file.open(QIODevice::ReadOnly)) {
        if (config.setContent(&file)) {
            rootAnswerStructure = config.documentElement();
        }
        file.close();
    }
}

/**
 * @brief Публичнй метод проверки лабы по паттерну Стратегия
 *        Запускаем одна за другой все проверки
 * @param variant - вариант лабораторной работы
 * @param code - присланный массив со строчками кода (классы присланного решения)
 * @return bool - true - все правильно, false - есть непоправимые ошибки
 */
bool StrategyLab::check(int variant, QList<QString>* code)
{
    if (this->checkByConfig(variant, code)
            && checkParentChildRelations(variant)
            && checkContext()
            && checkMainFunction()) {
        return true;
    }

    return false;
}

/**
 * @brief Здесь параллельно реализуется функицонал проверки кода по конфигу
 *        а также разделение кода на классы (divideIntoClasses)
 * @param code - присланное решение
 * @param node - конфиг
 * @return bool - результат проверки
 */
bool StrategyLab::checkByConfig(int variant, QList<QString> *code)
{
    // Заполняем QMap - divideIntoClasses
    /* вида
     * {
     *      "parent": "asdfsad"
     *      "children": (QList)[
     *          "sdfgsdfg",
     *          "sdfgsdfg",
     *          "sdfgdfgd"
     *      ],
     *      "context": "sdfgsdfg",
     *      "main": "dfasdfasd"
     * }
     */
    return true;
}

/**
 * @brief Проверки на абстрактный класс и его наследников
 * @return
 */
bool StrategyLab::checkParentChildRelations(int variant)
{
    // temp data
    QString parent = "class Strategy\n{\npublic:\nvirtual string DoAlgorithm() const = 0;\n};";
    QList<QString> children ({ "class Cash : public Strategy\n{\npublic:\nstring DoAlgorithm() const override\n{\nreturn \"Cash payment\";\n}\n};",
                               "class Card : public Strategy\n{\npublic:\nstring DoAlgorithm() const override\n{\nreturn \"Card payment\";\n}\n};",
                               "class Error : public Strategy\n{\npublic:\nstring DoAlgorithm() const override\n{\nreturn \"Error: invalid data\";\n}\n};" });

    /* Проверяем абстрактный класс */
    if (!parent.contains("public:")) {
        comments = "No public methods in abstract class, you should have at least one.";
        return false;
    }

    if (!parent.contains("virtual")) {
        comments = "No abstract methods inside your abstraact class. You should have at least one.";
        return false;
    }

    // TODO run more checks on abstract class

    /* Проверяем наседников */
    // Получаем конфиг нужной лабы
    QDomElement elem;
    foreach (QDomNode node, rootAnswerStructure.elementsByTagName("lab")) {
        elem = node.toElement();
        if (elem.attribute("number").toInt() == variant) break;
    }

    QDomElement abstract = elem.elementsByTagName("abstract").at(0).toElement();
    QString abstractClassName = abstract.attribute("name");
    QString abstractMethodName = abstract.elementsByTagName("method").at(0).toElement().attribute("name");
    QSet<QString> childMethodBodies;

    // Пробегаемся по наследникам
    foreach (QString child, children) {
        QString childClassName = child.left(child.indexOf("{")).split(" ", QString::SkipEmptyParts).at(1);
        if (!child.contains(abstractClassName)) {
            comments = "Class " + childClassName + " is not an instance of abstract class " + \
                    abstractClassName;
            return false;
        }

        QString betweenChildAndAbstarct = child.left(child.indexOf(abstractClassName));
        if (!betweenChildAndAbstarct.contains("public")) {
            QString modifier = betweenChildAndAbstarct.split(":").at(1).split(" ", QString::SkipEmptyParts).at(0);
            comments = "Your class " + childClassName + " instantiating abstract class " + \
                    abstractClassName + " with " + modifier + " modificator. It should be 'public'";
            return false;
        }

        if (!child.contains(abstractMethodName) || !child.contains("override")) {
            comments = "Your class " + childClassName + "does not override abstract method " + abstractMethodName + " that you \n" + \
                    " described inside abstract class " + abstractClassName;
            return false;
        }

        QString fromStartToAbstractMethod = child.left(child.indexOf(abstractMethodName));
        QString modifierForAbstractMethod = child.left(fromStartToAbstractMethod.lastIndexOf(":")).simplified();
        if (!modifierForAbstractMethod.split(" ", QString::SkipEmptyParts).endsWith("public")) {
            comments = "Overriden method " + abstractMethodName + " inside class " + childClassName + " should be public";
            return false;
        }

        QString methodBody = child.right(child.lastIndexOf(abstractMethodName));
        QString cutBodyToStart = methodBody.right(methodBody.indexOf("{"));
        QString cutBodyToEnd = cutBodyToStart.left(cutBodyToStart.lastIndexOf("}"));
        childMethodBodies.insert(cutBodyToEnd.simplified());
    }

    int heirsAmount = elem.elementsByTagName("heirs").at(0).toElement().attribute("amount").toInt();
    if (childMethodBodies.count() != heirsAmount) {
        comments = "Your classes that are instances of abstract class " + abstractClassName + " override\n" + \
                "abstract method " + abstractMethodName + " with the same implementation";
        return false;
    }

    return true;
}

/**
 * @brief Проверки на класс контекста
 * @return
 */
bool StrategyLab::checkContext()
{
    return true;
}

/**
 * @brief Проверки на основную функцию (int main)
 * @return
 */
bool StrategyLab::checkMainFunction()
{
    return true;
}

/**
 * @brief Деструктор
 */
StrategyLab::~StrategyLab()
{
    // TODO дописать
}
