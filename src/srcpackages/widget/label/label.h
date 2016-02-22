#ifndef LABEL_H
#define LABEL_H

#include <QLabel>
#include "labelobservable.h"
#include "models/components/abstractwidgethandler.h"
#include "models/components/abstractwidgetcontroller.h"

class Label: public QLabel, public LabelObservable, public AbstractWidgetHandler
{
    Q_OBJECT
public:
    Label();
    void SetText(int value);
    void SetText(std::string value);

signals:

private slots:

};

#endif // LABEL_H
