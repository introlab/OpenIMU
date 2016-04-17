#include "rangeslider.h"
#include <time.h>
#include <ctime>

RangeSlider::RangeSlider(QWidget *parent) : QWidget(parent)
{
    rightSlider = new QSlider();
    leftSlider = new QSlider();
    rightLabel = new QLabel();
    leftLabel = new QLabel();

    leftSlider->setOrientation(Qt::Orientation::Horizontal);
    rightSlider->setOrientation(Qt::Orientation::Horizontal);

    leftSlider->setContentsMargins(10,10,0,10);
    rightSlider->setContentsMargins(0,10,10,10);

    mainLayout = new QHBoxLayout();

    mainLayout->addWidget(leftLabel);
    mainLayout->addWidget(leftSlider);
    mainLayout->addWidget(rightSlider);
    mainLayout->addWidget(rightLabel);

    this->setLayout(mainLayout);

    connect(leftSlider,SIGNAL(valueChanged(int)),parent,SLOT(leftSliderValueChanged(int)));
    connect(rightSlider,SIGNAL(valueChanged(int)),parent,SLOT(rightSliderValueChanged(int)));

}
void RangeSlider::setRangeValues(int min, int max){
    leftSlider->setMinimum(min/1000);
    rightSlider->setMaximum(max/1000);
    rightSlider->setValue(max/1000);
}

void RangeSlider::setStartHour(int min){
    std::time_t _time =(time_t) min/1000;
    char buffer[32];
    std::strftime(buffer, 32, "%H:%M", gmtime (&_time));
    QString text;
    text.append("Heure de début: ");
    text.append(buffer);
    leftLabel->setText(text);
}

void RangeSlider::setEndHour(int max){
    std::time_t _time =(time_t) max/1000;
    char buffer[32];
    std::strftime(buffer, 32, "%H:%M", gmtime (&_time));
    QString text;
    text.append("Heure de fin: ");
    text.append(buffer);
    rightLabel->setText(text);
}
