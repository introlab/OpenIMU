#ifndef UTILITIES_H
#define UTILITIES_H

#include <string>
#include <qstring>
#include <fstream>
#include <iostream>
#include <QSoundEffect>

using namespace std;

enum MessageStatus { none = 0, success = 1, warning = 2, error = 3};

class Utilities
{
   public:
    static QString capitalizeFirstCharacter(QString myString);
    static QString capitalizeFirstCharacter(string myString);
    void playAudio(void);

    static std::string getColourFromEnum(MessageStatus status);

    static const std::string successColour;
    static const std::string errorColour;
    static const std::string warningColour;
    static const std::string defaultColour;
};

#endif // UTILITIES_H


