#ifndef DISPLAY_H
#define DISPLAY_H

#include <QWidget>
#include <list>
#include <QGridLayout>
#include "models/components/abstractwidgethandler.h"

class Display : public QWidget
{
    Q_OBJECT
public:
    explicit Display(QWidget *parent = 0);
    void setWidget(AbstractWidgetHandler *widget, int x, int y);

private:
    QGridLayout* gridLayout;

signals:

public slots:
};

#endif // DISPLAY_H
