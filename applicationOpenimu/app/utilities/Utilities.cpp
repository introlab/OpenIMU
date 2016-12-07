#include "Utilities.h"

using namespace std;

const QString Utilities::successColour = "#2ECC71 ";
const QString Utilities::errorColour = "#E84C3C ";
const QString Utilities::warningColour = "#F1C40F";
const QString Utilities::defaultColour = "#2C3E50";

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

    /*QSound notificationSound(":/audio/NotificationSound-2.wav");
    notificationSound.play();*/
}

QString Utilities::getColourFromEnum(MessageStatus status)
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





