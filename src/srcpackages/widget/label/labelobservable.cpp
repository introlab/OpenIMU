#include "labelobservable.h"

LabelObservable::LabelObservable()
{
}

void LabelObservable::SetObserver(LabelObserver *controller)
{
    this->controller = controller;
}
