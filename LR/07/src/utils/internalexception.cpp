#include "internalexception.h"


void InternalException::formatMessage(QString explanation, QString systemError)
{
    errorMessage = explanation;
    if (!systemError.isEmpty()) {
        errorMessage += "\n\n System output: \n " + systemError + "\n\n";
    }
}
