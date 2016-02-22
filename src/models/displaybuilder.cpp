#include "displaybuilder.h"
#include "packages/widgets/plot/plot.h"
#include "packages/widgets/plot/plotcontroller.h"

DisplayBuilder::DisplayBuilder()
{
    display = new Display();
}

AbstractWidgetController *DisplayBuilder::CreateWidget(std::string widgetName, int x, int y)
{
    QWidget* widget;
    AbstractWidgetController* wController;
    if(widgetName == "graph")
    {
        widget = new Plot();
        widgetList.push_back(widget);

        wController = new PlotController(widget);
    }
    else if(widgetName == "button")
    {

    }
}

Display *DisplayBuilder::GetDisplay()
{
    return display;
}

void DisplayBuilder::Clear()
{
    for (std::list<QWidget*>::const_iterator iterator = widgetList.begin(), end = widgetList.end(); iterator != end; ++iterator) {
        delete *iterator;
    }
    delete display;
}
