#include "utils.h"

#include <string>
#include <qstring>
#include <fstream>
#include <iostream>

using namespace std;

QString Utils::capitalizeFirstCharacter(QString myString)
{
    return myString.at(0).toUpper() + myString.mid(1);
}

QString Utils::capitalizeFirstCharacter(string myString)
{
    QString myQString = QString::fromStdString(myString);
    return myQString.at(0).toUpper() + myQString.mid(1);
}



