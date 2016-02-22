#ifndef BUTTON_H
#define BUTTON_H

#include <QPushButton>
#include "buttonobservable.h"
#include "models/components/abstractwidgethandler.h"
#include "models/components/abstractwidgetcontroller.h"

class Button: public QPushButton, public ButtonObservable, public AbstractWidgetHandler
{
    Q_OBJECT
public:
    Button();

signals:

private slots:
    void OnClick();
};

#endif // BUTTON_H
