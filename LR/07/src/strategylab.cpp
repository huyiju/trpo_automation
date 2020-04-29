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
bool StrategyLab::check(int variant, QList<QString> code)
{
    if (this->checkByConfig(variant, code)
            && checkParentChildrenRelations()
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
bool StrategyLab::checkByConfig(int variant, QList<QString> code)
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

    code.push_back("class Car\n{\npublic:\nvirtual string use() const = 0;\n};");
    code.push_back("class Cash : public Car\n{\npublic:\nstring use() const override\n{\nreturn \"Cash payment\";\n}\n};");
    code.push_back("class Card : public Car\n{\npublic:\nstring use() const override\n{\nreturn \"Card payment\";\n}\n};");
    code.push_back("class Error : public Car\n{\npublic:\nstring use() const override\n{\nreturn \"Error: invalid data\";\n}\n};");

    foreach (QString strClass, code) {
        if (!strClass.contains("class")) {
            classes.insert("main", strClass);
        } else if (strClass.left(strClass.indexOf("{")).simplified().split(" ").at(1) == abstractClassName) {
            classes.insert("parent", strClass);
        } else if (strClass.right(strClass.left(strClass.indexOf("{")).indexOf(":")).simplified().split(" ").at(1) == abstractClassName) {
            children.push_back(strClass);
        } else {
            classes.insert("context", strClass);
        }
    }

    return true;
}

/**
 * @brief Проверки на абстрактный класс и его наследников
 * @return
 */
bool StrategyLab::checkParentChildrenRelations()
{
    /***** Проверки на абстрактный класс *****/

    QString parent = classes.value("parent");

    // Проверка: абстрактный класс обладает абстрактным методом
    if (!parent.contains("virtual")) {
        comments = "No abstract methods inside your abstract class " + abstractClassName + ". You should have at least one.";
        return false;
    }

    // Проверка: абстрактный класс обладает абстрактным методом с модификатором public
    if (!checkAbstractMethodModifier(abstractClassName, parent)) {
        return false;
    }

    // Проверка: абстрактный класс обладает чистым абстрактным методом
    if (!parent.right(parent.indexOf(abstractMethodName)).simplified().split(" ").join("").contains("=0;")) {
        comments = "Your abstract method " + abstractMethodName + " is not declared as pure abstract.\n " + \
                "You should use '= 0' at the end of declaration";
        return false;
    }


    /***** Проверки на наследников абстрактного класса *****/

    if (!checkChildren()) {
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
bool StrategyLab::checkChildren()
{
    QSet<QString> childMethodBodies;

    foreach (QString child, children) {

        // Проверка: класс ребенок наследуется от родителя
        QString childClassName = child.left(child.indexOf("{")).split(" ", QString::SkipEmptyParts).at(1);
        if (!child.contains(abstractClassName)) {
            comments = "Class " + childClassName + " is not an instance of abstract class " + abstractClassName;
            return false;
        }

        // Проверка: класс ребенок наследуется от родителя черз модификтаор public
        QString betweenChildAndAbstarct = child.left(child.indexOf(abstractClassName));
        if (!betweenChildAndAbstarct.contains("public")) {
            QString modifier = betweenChildAndAbstarct.split(":").at(1).split(" ", QString::SkipEmptyParts).at(0);
            comments = "Your class " + childClassName + " instantiating abstract class " + \
                    abstractClassName + " with " + modifier + " modificator. It should be 'public'";
            return false;
        }

        // Проверка: класс ребенок переопределяет абстрактный метод родителя
        if (!child.contains(abstractMethodName) || !child.contains("override")) {
            comments = "Your class " + childClassName + "does not override abstract method " + abstractMethodName + " that you \n" + \
                    " described inside abstract class " + abstractClassName;
            return false;
        }

        // Проверка: класс ребенок переопределяет абстрактный метод родителя c модификатором public
        if (!checkAbstractMethodModifier(childClassName, child)) {
            return false;
        }

        // Закидываем тела переопределенных методов наследников в массив
        QString methodBody = child.right(child.lastIndexOf(abstractMethodName));
        QString cutBodyToStart = methodBody.right(methodBody.indexOf("{"));
        QString cutBodyToEnd = cutBodyToStart.left(cutBodyToStart.lastIndexOf("}"));
        childMethodBodies.insert(cutBodyToEnd.simplified());
    }

    // Проверка: реализации переопределенных методов наследников различаются
    if (childMethodBodies.count() != heirsAmount) {
        comments = "Your classes that are instances of abstract class " + abstractClassName + " override\n" + \
                "abstract method " + abstractMethodName + " with the same implementation";
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
bool StrategyLab::checkAbstractMethodModifier(QString className, QString classBody, QString modifier)
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
