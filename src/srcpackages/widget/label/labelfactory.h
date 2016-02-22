#ifndef LABELFACTORY_H
#define LABELFACTORY_H

#include "models/components/abstractwidgetfactory.h"

class LabelFactory: public AbstractWidgetFactory
{
public:
    LabelFactory();
    void Generate();
};

#endif // LABELFACTORY_H
