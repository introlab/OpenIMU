#include "labelfactory.h"
#include "label.h"
#include "labelcontroller.h"

LabelFactory::LabelFactory(): AbstractWidgetFactory()
{

}

void LabelFactory::Generate()
{
    this->widget = new Label();
    this->controller = new LabelController((Label*)this->widget);
}
