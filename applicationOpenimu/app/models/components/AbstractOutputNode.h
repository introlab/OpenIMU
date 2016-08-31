#ifndef ABSTRACTOUTPUTNODE_H
#define ABSTRACTOUTPUTNODE_H

#include "AbstractInputNode.h"
#include <vector>

class AbstractOutputNode
{
public:
    AbstractOutputNode();
    void Send(std::vector<int> value);
    void AddDest(AbstractInputNode *input);
    virtual std::string GetID(){return "";}
    void SetStringID(const std::string value);
    std::string GetStringID();
    std::vector<int> getValueBuf() const;
    void setValueBuf(std::vector<int> value);
	
protected:
    std::vector<int> valueBuf;
    virtual void NotifyAll() = 0;
    std::vector<AbstractInputNode*> inputs;

private:
    std::string stringID;
};

#endif // ABSTRACTOUTPUTNODE_H
