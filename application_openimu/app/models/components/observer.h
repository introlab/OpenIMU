#ifndef OBSERVER_H
#define OBSERVER_H

#include <iostream>

class Observer
{
public:
    Observer();
    virtual void Notify(std::string) = 0;
};

#endif // OBSERVER_H
