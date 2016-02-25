#include "lcdnumber.h"
#include <sstream>

LcdNumber::LcdNumber(): QLCDNumber()
{
    this->SetText(12);
}

void LcdNumber::SetText(int value)
{
    this->display(value);
}
