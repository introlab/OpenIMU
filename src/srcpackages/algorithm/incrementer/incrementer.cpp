#include "incrementer.h"
#include "models/components/inputnode.h"
#include "models/components/outputnode.h"

Incrementer::Incrementer()
{
    this->a = 0;
}

void Incrementer::Notify(std::string inputID)
{
    if(inputID == "click")
        work();
}

void Incrementer::work()
{
    ((OutputNode<int>*)this->Output("a"))->Send(a++);
}
