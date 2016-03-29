#ifndef OUTPUT_H
#define OUTPUT_H

#include "inputnode.h"
#include <vector>

class OutputNode
{
public:
    OutputNode();
    ~OutputNode();
    void Send(int value);
    void AddDest(InputNode *input);
    virtual std::string GetID(){return "";}
    void SetStringID(const std::string value);
    std::string GetStringID();


private:
    int valueBuf;
    std::vector<InputNode*> inputs;
    void NotifyAll();
    std::string stringID;
};

#endif // OUTPUT_H
