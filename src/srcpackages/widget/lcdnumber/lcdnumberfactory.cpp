#include "lcdnumberfactory.h"
#include "lcdnumber.h"
#include "lcdnumbercontroller.h"

LcdNumberFactory::LcdNumberFactory(): AbstractWidgetFactory()
{

}

void LcdNumberFactory::Generate()
{
    this->widget = new LcdNumber();
    this->controller = new LcdNumberlController((LcdNumber*)this->widget);
}
