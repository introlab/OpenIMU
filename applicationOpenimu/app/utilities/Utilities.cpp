#include "Utilities.h"

using namespace std;

const std::string Utilities::successColour = "#25FF3C";
const std::string Utilities::errorColour = "#FE0D0D";
const std::string Utilities::warningColour = "#FEFE08";
const std::string Utilities::defaultColour = "#000000";

QString Utilities::capitalizeFirstCharacter(QString myString)
{
    return myString.at(0).toUpper() + myString.mid(1);
}

QString Utilities::capitalizeFirstCharacter(string myString)
{
    QString myQString = QString::fromStdString(myString);
    return myQString.at(0).toUpper() + myQString.mid(1);
}

void Utilities::playAudio(void)
{
    QSoundEffect notificationAudio;
    notificationAudio.setSource(QUrl::fromLocalFile(":/audio/NotificationSound-2.wav"));
    notificationAudio.setVolume(0.75f);
    notificationAudio.play();
}

std::string Utilities::getColourFromEnum(MessageStatus status)
{
    switch(status)
    {
        case success:
            return successColour;
        case warning:
            return warningColour;
        case error:
            return errorColour;
        default:
            return defaultColour;
    }
}





