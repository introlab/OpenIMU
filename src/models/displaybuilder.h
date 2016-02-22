#ifndef WIDGETBUILDER_H
#define WIDGETBUILDER_H

#include "components/abstractwidgetcontroller.h"
#include "views/display.h"
#include <QWidget>

class DisplayBuilder
{
public:
    DisplayBuilder();

    AbstractWidgetController* CreateWidget(std::string widgetName, int x, int y);
    Display* GetDisplay();
    void Clear();

private:
    std::list<QWidget*> widgetList;
    Display* display;
};

#endif // WIDGETBUILDER_H
