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
      m_mainLayout = new QHBoxLayout;
      this->setLayout(m_mainLayout);
    }
    ~MainWidget();
    QHBoxLayout* m_mainLayout;

};

#endif
