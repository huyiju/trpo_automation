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
       Храниться в rootAnswerStructure*/
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
  * @brief Проверка присланного кода по конфигу
  * @return void
  */
void StrategyLab::checkConfig(int variant, QList<QString> *code)
{
    /* Выделяем конфиг для нужного варианта лабораторной работы */
    QDomNode node;
    QDomElement configLab;
    foreach (node, rootAnswerStructure.elementsByTagName("lab")) {
      configLab = node.toElement();
      if (configLab.attribute("number").toInt() == variant)
          break;
    }
    /* Проверка количества потомков */
    QString stringValue, temp;
    int heirsAmount;
    int pos;

    foreach (stringValue, code) {
       if (stringValue.indexOf(": public", 0) != -1 || stringValue.indexOf(":public", 0 ) != -1) {
           heirsAmount++;

        }

    }
    node = configLab.lastChild();
    if (configLab.attribute("heirs amount").toInt() == heirsAmount) {
        /* Записываем данные в QMap */
    }
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
