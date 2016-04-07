#ifndef OUTPUT_H
#define OUTPUT_H

#include "inputnode.h"
#include <vector>

class OutputNode
{
public:
    OutputNode();
    void Send(std::vector<int> value);
    void AddDest(InputNode *input);
    virtual std::string GetID(){return "";}
    void SetStringID(const std::string value);
    std::string GetStringID();
    std::vector<int> getValueBuf() const;
    void setValueBuf(std::vector<int> value);
	
protected:
    std::vector<int> valueBuf;

private:
    void NotifyAll();
    std::vector<InputNode*> inputs;
    std::string stringID;
};

#endif // OUTPUT_H
