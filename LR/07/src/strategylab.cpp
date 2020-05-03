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
 * @brief Здесь параллельно реализуется функицонал проверки кода по конфигу
 *        а также разделение кода на классы (divideIntoClasses)
 * @param variant - вариант лабораторной работы
 * @param code - присланное решение
 * TODO переписать это!!
 * @return
 */
void StrategyLab::checkByConfig(int variant, QList<QString> code)
{
    QDomElement elem;
    QDomNodeList labsConfig = rootAnswerStructure.elementsByTagName("lab");
    for (QDomNode node = labsConfig.at(0); !node.isNull(); node = node.nextSibling()) {
        elem = node.toElement();
        if (elem.attribute("number").toInt() == variant) break;
    }

    QDomElement abstract = elem.elementsByTagName("abstract").at(0).toElement();
    abstractClassName = abstract.attribute("name");
    abstractMethodName = abstract.elementsByTagName("method").at(0).toElement().attribute("name");
    heirsAmount = elem.elementsByTagName("heirs").at(0).toElement().attribute("amount").toInt();

    foreach (QString strClass, code) {
        if (!strClass.contains("class")) {
            classes.insert("main", strClass);
        } else if (strClass.left(strClass.indexOf("{")).simplified().split(" ").at(1) == abstractClassName) {
            classes.insert("parent", strClass);
        } else if (strClass.contains(abstractClassName)) {
            QString declare = strClass.left(strClass.indexOf("{"));
            if (declare.mid(declare.indexOf(":")).simplified().split(" ").at(2) == abstractClassName) {
                children.push_back(strClass);
            }
        } else {
            classes.insert("context", strClass);
        }
    }
}

/**
 * @brief Проверки на абстрактный класс и его наследников
 * @return
 */
void StrategyLab::checkParentChildrenRelations()
{
    /***** Проверки на абстрактный класс *****/

    QString parent = classes.value("parent");

    // Проверка: абстрактный класс обладает абстрактным методом
    if (!parent.contains("virtual")) {
        throw UnexpectedResultException("No abstract methods inside your abstract class '" + \
                                        abstractClassName + "'. You should have at least one.");
    }

    // Проверка: абстрактный класс обладает абстрактным методом с модификатором public
    checkAbstractMethodModifier(abstractClassName, parent);

    // Проверка: абстрактный класс обладает чистым абстрактным методом
    if (!parent.mid(parent.indexOf(abstractMethodName)).simplified().split(" ").join("").contains("=0;")) {
        throw UnexpectedResultException("Your abstract method '" + abstractMethodName + \
                                        "' is not declared as pure abstract.\n " + \
                                        "You should use '= 0' at the end of declaration");
    }

    /***** Проверки на наследников абстрактного класса *****/

    checkChildren();
}

/**
 * @brief Проверка каждого наследника (на престол), годятся?
 * @return
 */
void StrategyLab::checkChildren()
{
    QSet<QString> childMethodBodies;

    foreach (QString child, children) {

        // Проверка: класс ребенок наследуется от родителя
        QString childClassName = child.left(child.indexOf("{")).split(" ", QString::SkipEmptyParts).at(1);
        if (!child.contains(abstractClassName)) {
            throw UnexpectedResultException("Class '" + childClassName + \
                                            "' is not an instance of abstract class '" + abstractClassName + "'");
        }

        // Проверка: класс ребенок наследуется от родителя черз модификтаор public
        QString betweenChildAndAbstarct = child.left(child.indexOf(abstractClassName));
        if (!betweenChildAndAbstarct.contains("public")) {
            QString modifier = betweenChildAndAbstarct.split(":").at(1).split(" ", QString::SkipEmptyParts).at(0);
            throw UnexpectedResultException("Your class '" + childClassName + "' instantiating abstract class '" + \
                                            abstractClassName + "' with '" + modifier + " modificator. It should be 'public'");
        }

        // Проверка: класс ребенок переопределяет абстрактный метод родителя
        if (!child.contains(abstractMethodName) || !child.contains("override")) {
            throw UnexpectedResultException("Your class '" + childClassName + "' does not override abstract method '" + \
                                            abstractMethodName + "' that you \n described inside abstract class '" + \
                                            abstractClassName + "'");
        }

        // Проверка: класс ребенок переопределяет абстрактный метод родителя c модификатором public
        checkAbstractMethodModifier(childClassName, child);

        // Закидываем тела переопределенных методов наследников в массив
        QString methodBody = child.mid(child.lastIndexOf(abstractMethodName));
        QString cutBodyToStart = methodBody.mid(methodBody.indexOf("{"));
        QString cutBodyToEnd = cutBodyToStart.left(cutBodyToStart.lastIndexOf("}"));
        childMethodBodies.insert(cutBodyToEnd.simplified());
    }

    // Проверка: реализации переопределенных методов наследников различаются
    if (childMethodBodies.count() != heirsAmount) {
        throw UnexpectedResultException("Your classes that are instances of abstract class '" + \
                                        abstractClassName + "' override \n abstract method '" + \
                                        abstractMethodName + "' with the same implementation");
    }
}

/**
 * @brief Проверяет, чтобы модификатор метода в классе соответствовал указанному
 * @param className - имя класса
 * @param classBody - класс, где есть проверяемый метод
 * @param modifier - нужный модификатор
 * @return
 */
void StrategyLab::checkAbstractMethodModifier(QString className, QString classBody, QString modifier)
{
    QString fromStartToAbstractMethod = classBody.left(classBody.indexOf(abstractMethodName));
    QString modifierForAbstractMethod = classBody.left(fromStartToAbstractMethod.lastIndexOf(":")).simplified();
    if (!modifierForAbstractMethod.split(" ", QString::SkipEmptyParts).endsWith(modifier)) {
        throw UnexpectedResultException("Method '" + abstractMethodName + "' inside class '" + \
                                        className + "' should be '" + modifier + "'");
    }
}

/**
 * @brief Проверки на класс контекста
 * @return
 */
void StrategyLab::checkContext()
{
    return;
}

/**
 * @brief Проверки на основную функцию (int main)
 * @return
 */
void StrategyLab::checkMainFunction()
{
    return;
}

/**
 * @brief Деструктор
 */
StrategyLab::~StrategyLab()
{
    // TODO дописать
}
