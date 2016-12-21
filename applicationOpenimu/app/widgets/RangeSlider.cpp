#include "RangeSlider.h"
#include <time.h>
#include <ctime>
#include<QQuickView>
#include<QQuickItem>
#include<QSlider>

RangeSlider::RangeSlider(QWidget *parent) : QWidget(parent)
{
    m_rightLabel = new QLabel();
    m_leftLabel = new QLabel();

    m_mainLayout = new QHBoxLayout();
    m_refParent = parent;

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

    m_mainLayout->addWidget(m_leftLabel);
    m_mainLayout->addWidget(container);
    m_mainLayout->addWidget(m_rightLabel);
    m_mainLayout->setSpacing(0);
    this->setLayout(m_mainLayout);

    QSizePolicy spLeft(QSizePolicy::Preferred, QSizePolicy::Preferred);
    spLeft.setHorizontalStretch(1);
    m_leftLabel->setSizePolicy(spLeft);
    m_rightLabel->setSizePolicy(spLeft);

    QSizePolicy spRight(QSizePolicy::Preferred, QSizePolicy::Preferred);
    spRight.setHorizontalStretch(4);
    container->setSizePolicy(spRight);
}

void RangeSlider::setStartHour(long long min){
    std::time_t _time =(time_t) min;
    char buffer[32];
    std::strftime(buffer, 32, "%D - %H:%M:%S", gmtime (&_time));
    QString text;
    text.append(tr("Début: "));
    text.append(buffer);
    m_leftLabel->setText(text);
}

void RangeSlider::setEndHour(long long max){
    std::time_t _time =(time_t) max;
    char buffer[32];
    std::strftime(buffer, 32, "%D - %H:%M:%S", gmtime (&_time));
    QString text;
    text.append(tr("Fin: "));
    text.append(buffer);
    m_rightLabel->setText(text);
}
