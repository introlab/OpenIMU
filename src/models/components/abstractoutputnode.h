#ifndef ABSTRACTOUTPUTNODE_H
#define ABSTRACTOUTPUTNODE_H

#include <iostream>

class AbstractOutputNode
{
public:
    AbstractOutputNode();
    virtual std::string GetID(){return "";}
    void SetStringID(const std::string value);
    std::string GetStringID();

protected:
    std::string stringID;
};

#endif // ABSTRACTOUTPUTNODE_H
