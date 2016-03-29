#include "dateselectorlabel.h"


DateSelectorLabel::DateSelectorLabel(const QString& text, QWidget* parent)
    : QLabel(parent)
{
    setText(text);
}

DateSelectorLabel::~DateSelectorLabel()
{
}

void DateSelectorLabel::mousePressEvent(QMouseEvent* event)
{
    emit clicked(this->text().toStdString());
}
