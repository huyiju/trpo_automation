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
bool StrategyLab::checkParentChildrenRelations(int variant)
{
    // TODO выпилить
    // temp data
    QString parent = "class Strategy\n{\npublic:\nvirtual string DoAlgorithm() const = 0;\n};";
    QList<QString> children ({ "class Cash : public Strategy\n{\npublic:\nstring DoAlgorithm() const override\n{\nreturn \"Cash payment\";\n}\n};",
                               "class Card : public Strategy\n{\npublic:\nstring DoAlgorithm() const override\n{\nreturn \"Card payment\";\n}\n};",
                               "class Error : public Strategy\n{\npublic:\nstring DoAlgorithm() const override\n{\nreturn \"Error: invalid data\";\n}\n};" });
    // TODO выпилить
    // Получаем конфиг нужной лабы - такое будет в методе checkByConfig - там запись идет в приватные переменные
    QDomElement elem;
    foreach (QDomNode node, rootAnswerStructure.elementsByTagName("lab")) {
        elem = node.toElement();
        if (elem.attribute("number").toInt() == variant) break;
    }

    QDomElement abstract = elem.elementsByTagName("abstract").at(0).toElement();
    QString abstractClassName = abstract.attribute("name");
    QString abstractMethodName = abstract.elementsByTagName("method").at(0).toElement().attribute("name");

    if (!checkParent(parent, abstractMethodName, abstractClassName)) {
        return false;
    }

    int heirsAmount = elem.elementsByTagName("heirs").at(0).toElement().attribute("amount").toInt();
    if (!checkChildren(children, abstractClassName, abstractMethodName, heirsAmount)) {
        return false;
    }
}

/**
 * @brief Проверка абстрактного класса
 * @param parent - тело класса
 * @param methodName - имя абстрактного метода
 * @param className - имя класса
 * @todo выпилить className, methodName
 * @return
 */
bool StrategyLab::checkParent(QString parent, QString methodName, QString className)
{
    if (!parent.contains("virtual")) {
        comments = "No abstract methods inside your abstract class" + className + ". You should have at least one.";
        return false;
    }

    if (!checkAbstractMethodModifier(className, parent, methodName)) {
        return false;
    }

    if (parent.right(parent.indexOf(methodName)).split(" ").join("").contains("const=0;")) {
        comments = "Your abstract method " + methodName + " is not declared as pure abstract.\n " + \
                "You should use 'const = 0' at the end of declaration";
        return false;
    }

    return true;
}

/**
 * @brief Проверка каждого наследника (на престол), годятся?
 * @param children - список тел детёнышей
 * @param abstractClassName - имя абстрактного класса
 * @param methodName - имя абстрактного метода
 * @param heirsAmount - кол-во наследников
 * @todo выпилить heirsAmount, abstractClassName, methodName
 * @return
 */
bool StrategyLab::checkChildren(QList<QString> children, QString abstractClassName, QString methodName, int heirsAmount)
{
    QSet<QString> childMethodBodies;

    foreach (QString child, children) {
        QString childClassName = child.left(child.indexOf("{")).split(" ", QString::SkipEmptyParts).at(1);
        if (!child.contains(abstractClassName)) {
            comments = "Class " + childClassName + " is not an instance of abstract class " + abstractClassName;
            return false;
        }

        QString betweenChildAndAbstarct = child.left(child.indexOf(abstractClassName));
        if (!betweenChildAndAbstarct.contains("public")) {
            QString modifier = betweenChildAndAbstarct.split(":").at(1).split(" ", QString::SkipEmptyParts).at(0);
            comments = "Your class " + childClassName + " instantiating abstract class " + \
                    abstractClassName + " with " + modifier + " modificator. It should be 'public'";
            return false;
        }

        if (!child.contains(methodName) || !child.contains("override")) {
            comments = "Your class " + childClassName + "does not override abstract method " + methodName + " that you \n" + \
                    " described inside abstract class " + abstractClassName;
            return false;
        }

        if (!checkAbstractMethodModifier(childClassName, child, methodName)) {
            return false;
        }

        QString methodBody = child.right(child.lastIndexOf(methodName));
        QString cutBodyToStart = methodBody.right(methodBody.indexOf("{"));
        QString cutBodyToEnd = cutBodyToStart.left(cutBodyToStart.lastIndexOf("}"));
        childMethodBodies.insert(cutBodyToEnd.simplified());
    }

    if (childMethodBodies.count() != heirsAmount) {
        comments = "Your classes that are instances of abstract class " + abstractClassName + " override\n" + \
                "abstract method " + methodName + " with the same implementation";
        return false;
    }

    return true;
}

/**
 * @brief Проверяет, чтобы модификатор метода в классе соответствовал указанному
 * @param className - имя класса
 * @param abstractMethodName - имя абстрактного метода
 * @param class - класс, где есть проверяемый метод
 * @param modifier - нужный модификатор
 * @return
 */
bool StrategyLab::checkAbstractMethodModifier(QString className, QString classBody, QString abstractMethodName, QString modifier)
{
    QString fromStartToAbstractMethod = classBody.left(classBody.indexOf(abstractMethodName));
    QString modifierForAbstractMethod = classBody.left(fromStartToAbstractMethod.lastIndexOf(":")).simplified();
    if (!modifierForAbstractMethod.split(" ", QString::SkipEmptyParts).endsWith(modifier)) {
        comments = "Method " + abstractMethodName + " inside class " + className + " should be " + modifier;
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
