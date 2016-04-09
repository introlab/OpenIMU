#ifndef TOOLBARCONTROLLER_H
#define TOOLBARCONTROLLER_H


#include <QWidget>
#include <QMenuBar>
#include <QMainWindow>
#include <views/toolbarview.h>

class ToolbarController: public QWidget
{

public:
    ToolbarController();

    ToolbarView *toolbar = 0;
public slots:
    void openFile();
    void computeSteps();

};

#endif // TOOLBARCONTROLLER_H
