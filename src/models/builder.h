#ifndef DISPLAYBUILDER_H
#define DISPLAYBUILDER_H

#include <QWidget>
#include <string>
#include "views/display.h"
#include "jsonreader.h"
#include "components/abstractalgorithm.h"
#include "components/abstractinputnode.h"
#include "components/abstractoutputnode.h"
#include "components/abstractwidgetcontroller.h"


class Builder
{
public:
    Builder();
    Display* load(std::string str);
    JsonReader* jsonReader;

private:
    Display* display;
    std::list<AbstractWidgetController*> widgetList;
    std::list<AbstractInputNode*> inputNodeList;
    std::list<AbstractOutputNode*> outputNodeList;
    std::list<AbstractAlgorithm*> algorithmList;
};

#endif // DISPLAYBUILDER_H
