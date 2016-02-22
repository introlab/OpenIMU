#include "labelcontroller.h"
#include "models/components/outputnode.h"

LabelController::LabelController(Label *label)
{
    label->SetObserver(this);
}

void LabelController::Notify(std::string inputID)
{
    work();
}

void LabelController::work()
{
    int a = *((InputNode<int>*)this->Input("a"))->Get();
    ((Label*)this->widget)->SetText(a);
}
