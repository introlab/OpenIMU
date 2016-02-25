#ifndef LCDNUMBER_H
#define LCDNUMBER_H

#include <QLCDNumber>
#include "lcdnumberobservable.h"
#include "models/components/abstractwidgethandler.h"
#include "models/components/abstractwidgetcontroller.h"

class LcdNumber: public QLCDNumber, public LcdNumberObservable, public AbstractWidgetHandler
{
    Q_OBJECT
public:
    LcdNumber();
    void SetText(int value);

signals:

private slots:

};

#endif // LCDNUMBER_H
