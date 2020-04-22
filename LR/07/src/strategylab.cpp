#include "strategylab.h"

/**
 * @brief Конструктор
 * @param objectFromServer
 * @param parent
 */
StrategyLab::StrategyLab(QObject* parent)
    : QObject(parent)
{
    const QString fileName = "./config/answerStructure.xml";
    xmlFile.setFileName(fileName);
}

/**
 * @brief Публичнй метод проверки лабы по паттерну Стратегия
 * @param code - присланный массив со строчками кода (классы присланного решения)
 * @return bool - true - все правильно, false - есть непоправимые ошибки
 */
bool StrategyLab::check(const QList<QString> code)
{
//    QDomDocument domDoc;
//    bool result = false;

//    if (xmlFile.open(QIODevice::ReadOnly)) {
//        qDebug() << "opened";
//        if(domDoc.setContent(&xmlFile)) {
//            class QDomElement domElement= domDoc.documentElement();
//            result = this->checkInside(code, domElement);
//        }
//        xmlFile.close();

//        return result;
//    }

//    qDebug() << "exists: " << xmlFile.exists();
//    qDebug() << xmlFile.error() << " " << xmlFile.errorString();
//    throw QString("Ошибка сервера: не смогли прочитать конфиг для проверки");
    return true;
}

/**
 * @brief Метод, где идем вглубь конфига и сверяемся с присланным решением
 * @param code - присланное решение
 * @param node - конфиг
 * @return bool - результат проверки
 */
bool StrategyLab::checkInside(const QList<QString> code, const QDomNode& node)
{
    qDebug() << node.toElement().tagName();
    return true;
}

/**
 * @brief Деструктор
 */
StrategyLab::~StrategyLab()
{
    // TODO дописать
}
