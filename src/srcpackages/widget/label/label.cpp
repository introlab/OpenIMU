#include "label.h"
#include <sstream>

Label::Label(): QLabel()
{
    this->setText("LABEL!");
}

void Label::SetText(int value)
{
    this->setText(static_cast<std::ostringstream*>( &(std::ostringstream() << value) )->str().c_str());
}

void Label::SetText(std::string value)
{
    this->setText(value.c_str());
}
