#ifndef LABELCONTROLLER_H
#define LABELCONTROLLER_H

#include "labelobserver.h"
#include "models/components/abstractwidgetcontroller.h"
#include "label.h"

class LabelController: public LabelObserver, public AbstractWidgetController
{
public:
    LabelController(Label *label);
    void Notify(std::string inputID);
    void work();
};

#endif // LABELCONTROLLER_H
