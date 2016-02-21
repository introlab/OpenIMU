#ifndef DISPLAYBUILDER_H
#define DISPLAYBUILDER_H

#include <QWidget>
#include <string>
#include "views/display.h"
#include "layoutreader.h"


class DisplayBuilder
{
public:
    DisplayBuilder();
    Display* load(std::string str);
    LayoutReader* layoutReader;
};

#endif // DISPLAYBUILDER_H
