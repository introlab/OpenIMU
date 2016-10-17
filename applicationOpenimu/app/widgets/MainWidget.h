#ifndef MAINWIDGET_H
#define MAINWIDGET_H

#include <QWidget>
#include <QHBoxLayout>

class MainWidget : public QWidget {
    Q_OBJECT

public:
    MainWidget(QWidget *parent):
    QWidget(parent)
    {
      this->setStyleSheet("background-color:rgba(230, 233, 239,0.2);");
      mainLayout = new QHBoxLayout;
      this->setLayout(mainLayout);
    }
    ~MainWidget();
    QHBoxLayout* mainLayout;

};

#endif
