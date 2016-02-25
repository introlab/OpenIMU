#ifndef LCDNUMBERCONTROLLER_H
#define LCDNUMBERCONTROLLER_H

#include "lcdnumberobserver.h"
#include "models/components/abstractwidgetcontroller.h"
#include "lcdnumber.h"

class LcdNumberlController: public LcdNumberObserver, public AbstractWidgetController
{
public:
    LcdNumberlController(LcdNumber *lcdNumber);
    void Notify(std::string inputID);
    void work();
};

#endif // LCDNUMBERCONTROLLER_H
