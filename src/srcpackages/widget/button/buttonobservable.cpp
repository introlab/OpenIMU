#include "buttonobservable.h"

ButtonObservable::ButtonObservable()
{
}

void ButtonObservable::SetObserver(ButtonObserver *controller)
{
    this->controller = controller;
}

void ButtonObservable::NotifyClick()
{
    controller->NotifyClick();
}
