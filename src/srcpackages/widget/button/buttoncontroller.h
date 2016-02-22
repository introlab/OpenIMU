#ifndef BUTTONCONTROLLER_H
#define BUTTONCONTROLLER_H

#include "buttonobserver.h"
#include "models/components/abstractwidgetcontroller.h"
#include "button.h"

class ButtonController: public ButtonObserver, public AbstractWidgetController
{
public:
    ButtonController(Button *button);
    void NotifyClick();
    void Notify(std::string inputID);
    void work();
};

#endif // BUTTONCONTROLLER_H
