#include "graphobservable.h"

GraphObservable::GraphObservable()
{
}

void GraphObservable::SetObserver(GraphObserver *controller)
{
    this->controller = controller;
}
