#ifndef BUTTONFACTORY_H
#define BUTTONFACTORY_H

#include "models/components/abstractwidgetfactory.h"

class ButtonFactory: public AbstractWidgetFactory
{
public:
    ButtonFactory();
    void Generate();
};

#endif // BUTTONFACTORY_H
