#ifndef GRAPHOBSERVABLE_H
#define GRAPHOBSERVABLE_H

#include "graphobserver.h"

class GraphObservable: public GraphObserver
{
public:
    GraphObservable();
    void SetObserver(GraphObserver* controller);

protected:

    GraphObserver* controller;
};

#endif // GRAPHOBSERVABLE_H
