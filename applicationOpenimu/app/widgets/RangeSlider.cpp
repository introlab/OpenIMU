#include "RangeSlider.h"
#include <time.h>
#include <ctime>
#include<QQuickView>
#include<QQuickItem>
#include<QSlider>
#include <QQmlEngine>
#include <QApplication>
#include <QMainWindow>
#include <QSpacerItem>

RangeSlider::RangeSlider(QWidget *parent) : QWidget(parent)
{


    m_rightLabel = new QLabel(this);
    m_leftLabel = new QLabel(this);

    m_mainLayout = new QHBoxLayout(this);
    m_refParent = parent;

    QQuickView *view = new QQuickView();

    //view->setSurfaceType(QSurface::RasterSurface);

    view->engine()->addImportPath(QApplication::applicationDirPath() + "/qml");
    //qDebug() << view->engine()->importPathList();

    QWidget *container = QWidget::createWindowContainer(view, this);

    container->setMinimumSize(400, 50);
    container->setMaximumSize(400, 50);
    //container->setFocusPolicy(Qt::TabFocus);
    view->setSource(QUrl("qrc:/rangeSlider.qml"));
    container->show();
    view->show();


    // Get pointers to first and second values in range slider
    QQuickItem *object = view->rootObject();



    QObject::connect(object, SIGNAL(firstUpdated(QVariant)),parent, SLOT(firstUpdated(QVariant)));
    QObject::connect(object, SIGNAL(secondUpdated(QVariant)),parent, SLOT(secondUpdated(QVariant)));

    m_mainLayout->addSpacerItem(new QSpacerItem(10,0,QSizePolicy::MinimumExpanding));
    m_mainLayout->addWidget(m_leftLabel);
    m_mainLayout->addWidget(container);
    m_mainLayout->addWidget(m_rightLabel);
    m_mainLayout->addSpacerItem(new QSpacerItem(10,0,QSizePolicy::MinimumExpanding));
    this->setLayout(m_mainLayout);


    QSizePolicy spLeft(QSizePolicy::Preferred, QSizePolicy::Preferred);
    //spLeft.setHorizontalStretch(1);
    m_leftLabel->setSizePolicy(spLeft);
    m_rightLabel->setSizePolicy(spLeft);


    //QSizePolicy spRight(QSizePolicy::Preferred, QSizePolicy::Preferred);
    //spRight.setHorizontalStretch(4);
    //container->setSizePolicy(spRight);

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
