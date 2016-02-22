#include "button.h"

Button::Button(): QPushButton()
{
    this->setText("This is a test!");
    connect(this, SIGNAL(clicked()),this, SLOT(OnClick()));
}

void Button::OnClick()
{
    this->NotifyClick();
}
