#include "abstractwidgetfactory.h"

AbstractWidgetFactory::AbstractWidgetFactory()
{
}

AbstractWidgetHandler *AbstractWidgetFactory::GetWidget()
{
    return widget;
}

AbstractWidgetController *AbstractWidgetFactory::GetController()
{
    return controller;
}
