#include "lcdnumbercontroller.h"
#include "models/components/outputnode.h"

LcdNumberlController::LcdNumberlController(LcdNumber *lcdNumber)
{
    lcdNumber->SetObserver(this);
}

void LcdNumberlController::Notify(std::string inputID)
{
    work();
}

void LcdNumberlController::work()
{
    int a = *(int*)((InputNode<int>*)this->Input("input"))->Get();
    ((LcdNumber*)this->widget)->SetText(a);
}
