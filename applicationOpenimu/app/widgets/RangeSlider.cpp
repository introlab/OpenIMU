#include "RangeSlider.h"
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
    mainLayout->addWidget(rightLabel);
    mainLayout->addStretch();
    this->setLayout(mainLayout);

    connect(leftSlider,SIGNAL(valueChanged(int)),parent,SLOT(leftSliderValueChanged(int)));
    connect(rightSlider,SIGNAL(valueChanged(int)),parent,SLOT(rightSliderValueChanged(int)));

}
void RangeSlider::setRangeValues(long long min, long long max){
    leftSlider->setMinimum(min);
    leftSlider->setMaximum(max);
    rightSlider->setMaximum(max);
    rightSlider->setMinimum(min);
    rightSlider->setValue(max);
}

void RangeSlider::setStartHour(long long min){
    std::time_t _time =(time_t) min;
    char buffer[32];
    std::strftime(buffer, 32, "%H:%M", gmtime (&_time));
    QString text;
    text.append(tr("Heure de début: "));
    text.append(buffer);
    leftLabel->setText(text);
}

void RangeSlider::setEndHour(long long max){
    std::time_t _time =(time_t) max;
    char buffer[32];
    std::strftime(buffer, 32, "%H:%M", gmtime (&_time));
    QString text;
    text.append(tr("Heure de fin: "));
    text.append(buffer);
    rightLabel->setText(text);
}
