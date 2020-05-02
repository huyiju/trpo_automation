#include "internalexception.h"

/**
 * @brief Метод формирует
 * @param explanation - человеческое оъяснение проблемы
 * @param systemError - системный вывод сообщения об ошибке
 */
void InternalException::formatMessage(QString explanation, QString systemError)
{
    errorMessage = explanation;
    if (!systemError.isEmpty()) {
        errorMessage += "\n\n System output: \n " + systemError + "\n\n";
    }
}
