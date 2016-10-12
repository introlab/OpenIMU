#include "RangeSlider.h"
#include <time.h>
#include <ctime>
#include<QQuickView>
#include<QQuickItem>
#include<QSlider>

RangeSlider::RangeSlider(QWidget *parent) : QWidget(parent)
{
    rightLabel = new QLabel();
    leftLabel = new QLabel();

    mainLayout = new QHBoxLayout();
    refParent = parent;

    QQuickView *view = new QQuickView();
    QWidget *container = QWidget::createWindowContainer(view, this);
    container->setMinimumSize(40,40);
    container->setMaximumSize(400, 50);
    container->setFocusPolicy(Qt::TabFocus);
    view->setSource(QUrl("../applicationOpenImu/app/rangeSlider.qml"));

    // Get pointers to first and second values in range slider
    QQuickItem *object = view->rootObject();

    QObject::connect(object, SIGNAL(firstUpdated(QVariant)),parent, SLOT(firstUpdated(QVariant)));
    QObject::connect(object, SIGNAL(secondUpdated(QVariant)),parent, SLOT(secondUpdated(QVariant)));

    mainLayout->addWidget(leftLabel);
    mainLayout->addWidget(container);
    mainLayout->addWidget(rightLabel);
    mainLayout->setSpacing(0);
    this->setLayout(mainLayout);

    QSizePolicy spLeft(QSizePolicy::Preferred, QSizePolicy::Preferred);
    spLeft.setHorizontalStretch(1);
    leftLabel->setSizePolicy(spLeft);
    rightLabel->setSizePolicy(spLeft);

    QSizePolicy spRight(QSizePolicy::Preferred, QSizePolicy::Preferred);
    spRight.setHorizontalStretch(4);
    container->setSizePolicy(spRight);
}

void RangeSlider::setStartHour(long long min){
    std::time_t _time =(time_t) min;
    char buffer[32];
    std::strftime(buffer, 32, "%H:%M", gmtime (&_time));
    QString text;
    text.append(tr("Début: "));
    text.append(buffer);
    leftLabel->setText(text);
}

void RangeSlider::setEndHour(long long max){
    std::time_t _time =(time_t) max;
    char buffer[32];
    std::strftime(buffer, 32, "%H:%M", gmtime (&_time));
    QString text;
    text.append(tr("Fin: "));
    text.append(buffer);
    rightLabel->setText(text);
}
