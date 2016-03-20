#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <qwt_plot.h>
#include <string>

namespace Ui {
     class Widget;
}

class Widget : public QwtPlot {
     Q_OBJECT
public:
     Widget(QWidget *parent = 0);
     ~Widget();
    void setFolderPath(std::string path);
    void setupPlot();
protected:
     void changeEvent(QEvent *e);

private:
     Ui::Widget *ui;
     std::string m_folderPath;
};

#endif // WIDGET_H
