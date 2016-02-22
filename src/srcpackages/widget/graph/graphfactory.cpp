#include "graphfactory.h"
#include "graph.h"
#include "graphcontroller.h"

GraphFactory::GraphFactory(): AbstractWidgetFactory()
{

}

void GraphFactory::Generate()
{
    this->widget = new Graph();
    this->controller = new GraphController((Graph*)this->widget);
}
