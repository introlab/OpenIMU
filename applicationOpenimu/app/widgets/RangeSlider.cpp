#include "RangeSlider.h"
#include <time.h>
#include <ctime>
#include<QQuickView>
#include<QQuickItem>

RangeSlider::RangeSlider(QWidget *parent) : QWidget(parent)
{
 // rightSlider = new QSlider();
 // leftSlider = new QSlider();
    rightLabel = new QLabel();
    leftLabel = new QLabel();

 //   leftSlider->setOrientation(Qt::Orientation::Horizontal);
 //   rightSlider->setOrientation(Qt::Orientation::Horizontal);

 //   leftSlider->setContentsMargins(10,10,0,10);
 //   rightSlider->setContentsMargins(0,10,10,10);

    mainLayout = new QHBoxLayout();

    QQuickView *view = new QQuickView();
    QWidget *container = QWidget::createWindowContainer(view, this);
    container->setMinimumSize(40,40);
    container->setMaximumSize(400, 50);
    container->setFocusPolicy(Qt::TabFocus);
    view->setSource(QUrl("../applicationOpenImu/app/rangeSlider.qml"));
    QObject *object = view->rootObject();
    QObject::connect(object, SIGNAL(qmlSignal(QVariant)),this, SLOT(cppSlot(QVariant)));

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

    //connect(leftSlider,SIGNAL(valueChanged(int)),parent,SLOT(leftSliderValueChanged(int)));
    //connect(rightSlider,SIGNAL(valueChanged(int)),parent,SLOT(rightSliderValueChanged(int)));

}

void RangeSlider:: cppSlot(const QVariant &v) {
      qDebug() << "Called the C++ slot with value:" << v;

    /*  QQuickItem *item =
          qobject_cast<QQuickItem*>(v.value<QObject*>());
      qDebug() << "Item dimensions:" << item->width()
               << item->height();*/
   }

void RangeSlider::setLeftSliderRange(long long min, long long max){
  //  if(leftSlider)
  //  {
  //      leftSlider->setMinimum(0);
  //      leftSlider->setMaximum(10);
  //  }
}
void RangeSlider::setRightSliderRange(long long min, long long max){
  //  rightSlider->setMaximum(10);
 //   rightSlider->setMinimum(0);
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
