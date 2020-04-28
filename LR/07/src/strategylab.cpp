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
            && checkParentChildRelations()
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
    // Заполняем QMap
    return true;
}

/**
 * @brief Проверки на абстрактный класс и его наследников
 * @return
 */
bool StrategyLab::checkParentChildRelations()
{
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
