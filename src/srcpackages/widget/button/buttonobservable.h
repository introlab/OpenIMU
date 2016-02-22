#ifndef BUTTONOBSERVABLE_H
#define BUTTONOBSERVABLE_H

#include "buttonobserver.h"

class ButtonObservable: public ButtonObserver
{
public:
    ButtonObservable();
    void SetObserver(ButtonObserver* controller);

protected:
    void NotifyClick();

    ButtonObserver* controller;
};

#endif // BUTTONOBSERVABLE_H
