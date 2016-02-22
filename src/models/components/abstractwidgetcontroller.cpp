#include "abstractwidgetcontroller.h"

AbstractWidgetController::AbstractWidgetController()
{

}

void AbstractWidgetController::SetWidget(QWidget *newWidget)
{
    if (this->widget != 0)
        delete this->widget;
    this->widget = newWidget;
}
