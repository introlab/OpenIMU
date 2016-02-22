#ifndef IALGO_H
#define IALGO_H

#include <iostream>
#include <vector>
#include "abstractinputnode.h"
#include "abstractoutputnode.h"
#include "observer.h"

class AbstractAlgorithm : public Observer
{
public:
    AbstractAlgorithm();
    ~AbstractAlgorithm();
    virtual void Notify(std::string inputID);
    void AddInput(AbstractInputNode* input);
    void AddOutput(AbstractOutputNode* output);

    std::string GetStringID();
    void SetStringID(const std::string value);

protected:
    AbstractInputNode* Input(std::string inputID);
    AbstractOutputNode* Output(std::string outputID);


    std::vector<AbstractInputNode*> inputs;
    std::vector<AbstractOutputNode*> outputs;
    virtual void work() = 0;

    std::string stringID;

};

#endif // IALGO_H
