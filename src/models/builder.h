#ifndef DISPLAYBUILDER_H
#define DISPLAYBUILDER_H

#include <QWidget>
#include <string>
#include "views/display.h"
#include "jsonreader.h"


class Builder
{
public:
    Builder();
    Display* load(std::string str);
    JsonReader* layoutReader;
};

#endif // DISPLAYBUILDER_H
