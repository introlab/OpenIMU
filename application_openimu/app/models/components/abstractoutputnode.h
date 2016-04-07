#ifndef ABSTRACTOUTPUTNODE_H
#define ABSTRACTOUTPUTNODE_H

#include "abstractinputnode.h"
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
    void NotifyAll();

private:
    std::vector<AbstractInputNode*> inputs;
    std::string stringID;
};

#endif // ABSTRACTOUTPUTNODE_H
