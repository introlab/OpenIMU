#include "buttoncontroller.h"

ButtonController::ButtonController(Button *button)
{
    button->SetObserver(this);
}

void ButtonController::NotifyClick()
{
    std::cout<<"CLICKED!"<<std::endl;
}

void ButtonController::Notify(std::string inputID)
{
    work();
}

void ButtonController::work()
{

}
