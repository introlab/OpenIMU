#ifndef WIDGETBUILDER_H
#define WIDGETBUILDER_H

#include "components/abstractwidgetcontroller.h"
#include "components/abstractwidgethandler.h"
#include "views/display.h"
#include "jsonreader.h"
#include <QWidget>

class DisplayBuilder
{
public:
    DisplayBuilder();
    AbstractWidgetController* CreateWidget(std::string widgetName, int x, int y);
    Display* GetDisplay();
    void Clear();

private:
    void CreateItems();

    std::list<AbstractWidgetHandler*> widgetList;


    Display* display;
};

#endif // WIDGETBUILDER_H
