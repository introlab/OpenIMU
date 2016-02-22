#ifndef ABSTRACTWIDGETCONTROLLER_H
#define ABSTRACTWIDGETCONTROLLER_H

#include "abstractalgorithm.h"
#include <QWidget>

class AbstractWidgetController: public AbstractAlgorithm
{
public:
    AbstractWidgetController();
    void SetWidget(QWidget* newWidget);

private:
    QWidget* widget;
};

#endif // ABSTRACTWIDGETCONTROLLER_H
