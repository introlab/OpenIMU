#ifndef ABSTRACTWIDGETCONTROLLER_H
#define ABSTRACTWIDGETCONTROLLER_H

#include "abstractalgorithm.h"
#include <QWidget>

class AbstractWidgetController: public AbstractAlgorithm
{
public:
    AbstractWidgetController();
    void SetWidget(QWidget* newWidget);
    virtual void Notify(std::string inputID);

protected:
    QWidget* widget;
    virtual void work() = 0;
};

#endif // ABSTRACTWIDGETCONTROLLER_H
