#ifndef LCDNUMBEROBSERVABLE_H
#define LCDNUMBEROBSERVABLE_H

#include "lcdnumberobserver.h"

class LcdNumberObservable: public LcdNumberObserver
{
public:
    LcdNumberObservable();
    void SetObserver(LcdNumberObserver* controller);

protected:

    LcdNumberObserver* controller;
};

#endif // LCDNUMBEROBSERVABLE_H
