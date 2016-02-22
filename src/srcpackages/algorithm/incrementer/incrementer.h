#ifndef INCREMENTER_H
#define INCREMENTER_H

#include "models/components/abstractalgorithm.h"

class Incrementer: public AbstractAlgorithm
{
public:
    Incrementer();
    void Notify(std::string inputID);
    void work();

private:
    int a;
};

#endif // INCREMENTER_H
