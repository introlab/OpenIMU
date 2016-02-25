#ifndef LCDNUMBERFACTORY_H
#define LCDNUMBERFACTORY_H

#include "models/components/abstractwidgetfactory.h"

class LcdNumberFactory: public AbstractWidgetFactory
{
public:
    LcdNumberFactory();
    void Generate();
};

#endif // LCDNUMBERFACTORY_H
