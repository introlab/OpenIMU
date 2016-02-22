#include "buttoncontroller.h"
#include "models/components/outputnode.h"

ButtonController::ButtonController(Button *button)
{
    button->SetObserver(this);
}

void ButtonController::NotifyClick()
{
    work();
}

void ButtonController::Notify(std::string inputID)
{
    work();
}

void ButtonController::work()
{
    std::cout<<"CLICKED!"<<std::endl;
    ((OutputNode<int>*)this->Output("click"))->Send(54321);
}
