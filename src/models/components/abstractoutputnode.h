#ifndef ABSTRACTOUTPUTNODE_H
#define ABSTRACTOUTPUTNODE_H

#include <iostream>

class AbstractOutputNode
{
public:
    AbstractOutputNode();
    virtual std::string GetID(){return "";}
};

#endif // ABSTRACTOUTPUTNODE_H
