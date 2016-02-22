#include "display.h"

Display::Display(QWidget *parent) : QWidget(parent)
{
    this->gridLayout = new QGridLayout();
    this->setLayout(this->gridLayout);
}

void Display::setWidget(AbstractWidgetHandler *widget, int x, int y)
{
    this->gridLayout->addWidget((QWidget*)widget, x, y);
}
