#ifndef DISPLAYBUILDER_H
#define DISPLAYBUILDER_H

#include <QWidget>
#include <string>
#include "views/display.h"
#include "jsonreader.h"


class DisplayBuilder
{
public:
    DisplayBuilder();
    Display* load(std::string str);
    JsonReader* layoutReader;
};

#endif // DISPLAYBUILDER_H
