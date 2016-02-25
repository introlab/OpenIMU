#include "lcdnumberobservable.h"

LcdNumberObservable::LcdNumberObservable()
{
}

void LcdNumberObservable::SetObserver(LcdNumberObserver *controller)
{
    this->controller = controller;
}
