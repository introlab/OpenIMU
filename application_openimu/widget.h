#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <qwt_plot.h>

namespace Ui {
     class Widget;
}

class Widget : public QwtPlot {
     Q_OBJECT
public:
     Widget(QWidget *parent = 0);
     ~Widget();

protected:
     void changeEvent(QEvent *e);

private:
     Ui::Widget *ui;
     void setupPlot();
};

#endif // WIDGET_H
