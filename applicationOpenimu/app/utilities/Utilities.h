#ifndef UTILITIES_H
#define UTILITIES_H

#include <string>
#include <qstring>
#include <fstream>
#include <iostream>

using namespace std;

class Utilities
{
   public:
    static QString capitalizeFirstCharacter(QString myString);
    static QString capitalizeFirstCharacter(string myString);
};

#endif // UTILITIES_H


