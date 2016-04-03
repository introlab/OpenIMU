#include "dateselectorlabel.h"


DateSelectorLabel::DateSelectorLabel(const QString& text, QWidget* parent)
    : QLabel(parent)
{
    this->setMaximumHeight(20);
    QFont f( "Arial", 8, QFont::ExtraLight);
    this->setFont(f);

    std::string s = text.toStdString();
    char sep = '/';
    size_t i = s.rfind(sep, s.length());
    std::string t;
    if (i != std::string::npos) {
     t=s.substr(i+1, s.length() - i);
    }
    std::size_t found = t.find_last_of("/\\");
    t= t.substr(found+1) ;

    setText((QString)t.c_str());
    fullPath = text.toStdString();
}

DateSelectorLabel::~DateSelectorLabel()
{
}

void DateSelectorLabel::mousePressEvent(QMouseEvent* event)
{
    emit clicked(fullPath);
}
