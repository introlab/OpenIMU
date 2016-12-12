#ifndef UTILITIES_H
#define UTILITIES_H

#include <string>
#include <qstring>
#include <fstream>
#include <iostream>
#include <QSoundEffect>
#include <QSound>
#include <QDebug>

using namespace std;

enum MessageStatus { none = 0, success = 1, warning = 2, error = 3};

class Utilities
{
   public:
    static QString capitalizeFirstCharacter(QString myString);
    static QString capitalizeFirstCharacter(string myString);
    void playAudio(void);

    static QString getColourFromEnum(MessageStatus status);

    static const QString successColour;
    static const QString errorColour;
    static const QString warningColour;
    static const QString defaultColour;
};

#endif // UTILITIES_H


