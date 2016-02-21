#ifndef DISPLAY_H
#define DISPLAY_H

#include <QWidget>
#include <list>
#include <QGridLayout>

class Display : public QWidget
{
    Q_OBJECT
public:
    explicit Display(QWidget *parent = 0);
    void setWidget(QWidget* qWidget,int x,int y);
    QWidget* getWidget(int x,int y);

private:
    std::list<QWidget*> listW;
    //<QWidget*> listWidget;
    QGridLayout gridLayout;

signals:

public slots:
};

#endif // DISPLAY_H
