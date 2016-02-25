#include "displaybuilder.h"
#include "components/abstractwidgetfactory.h"

#include "srcpackages/widget/button/buttonfactory.h"
#include "srcpackages/widget/label/labelfactory.h"
#include "srcpackages/widget/graph/graphfactory.h"
#include "srcpackages/widget/lcdnumber/lcdnumberfactory.h"

DisplayBuilder::DisplayBuilder()
{
    this->display = new Display();
}

AbstractWidgetController *DisplayBuilder::CreateWidget(std::string widgetName, int x, int y)
{
    AbstractWidgetHandler* widget;
    AbstractWidgetController* wController;
    AbstractWidgetFactory* factory;
    if(widgetName == "Button")
    {
        factory = new ButtonFactory();
    }
    else if(widgetName == "Label")
    {
        factory = new LabelFactory();
    }
    else if(widgetName == "Graph")
    {
        factory = new GraphFactory();
    }
    else if(widgetName == "LCD")
    {
        factory = new LcdNumberFactory();
    }
    else {
        return 0;
    }

    factory->Generate();
    widget = factory->GetWidget();
    widgetList.push_back(widget);
    display->setWidget(widget, x, y);
    return factory->GetController();

}

Display *DisplayBuilder::GetDisplay()
{
    return display;
}

void DisplayBuilder::Clear()
{
    for (std::list<AbstractWidgetHandler*>::const_iterator iterator = widgetList.begin(), end = widgetList.end(); iterator != end; ++iterator) {
        delete *iterator;
    }
    delete display;
}
