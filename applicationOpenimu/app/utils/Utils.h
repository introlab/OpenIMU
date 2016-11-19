#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <qstring>
#include <fstream>
#include <iostream>

using namespace std;

class Utils
{
   public:
    static QString capitalizeFirstCharacter(QString myString);
    static QString capitalizeFirstCharacter(string myString);
};

#endif // UTILS_H


