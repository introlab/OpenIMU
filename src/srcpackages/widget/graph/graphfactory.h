#ifndef GRAPHFACTORY_H
#define GRAPHFACTORY_H

#include "models/components/abstractwidgetfactory.h"

class GraphFactory: public AbstractWidgetFactory
{
public:
    GraphFactory();
    void Generate();
};

#endif // GRAPHFACTORY_H
