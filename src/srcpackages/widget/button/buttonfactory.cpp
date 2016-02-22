#include "buttonfactory.h"
#include "button.h"
#include "buttoncontroller.h"

ButtonFactory::ButtonFactory(): AbstractWidgetFactory()
{

}

void ButtonFactory::Generate()
{
    this->widget = new Button();
    this->controller = new ButtonController((Button*)this->widget);
}
