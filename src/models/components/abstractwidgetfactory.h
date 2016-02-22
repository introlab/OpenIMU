#ifndef ABSTRACTWIDGETFACTORY_H
#define ABSTRACTWIDGETFACTORY_H

#include "abstractwidgetcontroller.h"
#include "abstractwidgethandler.h"

class AbstractWidgetFactory
{
public:
    AbstractWidgetFactory();
    virtual void Generate() = 0;
    virtual AbstractWidgetHandler* GetWidget();
    virtual AbstractWidgetController* GetController();

protected:
    AbstractWidgetHandler* widget;
    AbstractWidgetController* controller;
};

#endif // ABSTRACTWIDGETFACTORY_H
