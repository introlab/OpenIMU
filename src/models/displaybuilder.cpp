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
    if(widgetName == "Button")
    {
        AbstractWidgetFactory* factory = new ButtonFactory();
        factory->Generate();
        widget = factory->GetWidget();
        widgetList.push_back(widget);
        display->setWidget(widget, x, y);

        return factory->GetController();
    }
    else if(widgetName == "Label")
    {
        AbstractWidgetFactory* factory = new LabelFactory();
        factory->Generate();
        widget = factory->GetWidget();
        widgetList.push_back(widget);
        display->setWidget(widget, x, y);

        return factory->GetController();
    }
    else if(widgetName == "Graph")
    {
        AbstractWidgetFactory* factory = new GraphFactory();
        factory->Generate();
        widget = factory->GetWidget();
        widgetList.push_back(widget);
        display->setWidget(widget, x, y);

        return factory->GetController();
    }
    else if(widgetName == "LCD")
    {
        AbstractWidgetFactory* factory = new LcdNumberFactory();
        factory->Generate();
        widget = factory->GetWidget();
        widgetList.push_back(widget);
        display->setWidget(widget, x, y);

        return factory->GetController();
    }
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
