#ifndef LABELOBSERVABLE_H
#define LABELOBSERVABLE_H

#include "labelobserver.h"

class LabelObservable: public LabelObserver
{
public:
    LabelObservable();
    void SetObserver(LabelObserver* controller);

protected:

    LabelObserver* controller;
};

#endif // LABELOBSERVABLE_H
