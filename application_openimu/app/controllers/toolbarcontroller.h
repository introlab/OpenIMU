#ifndef TOOLBARCONTROLLER_H
#define TOOLBARCONTROLLER_H


#include <QWidget>
#include <QMenuBar>
#include <QMainWindow>
#include <views/toolbarview.h>

class ToolbarController: public QObject
{
public:
    ToolbarController(QWidget *parent = 0);

    ToolbarView getToolbar() const;
    void setToolbar(const ToolbarView &value);

public slots:
    void openFile();
    void computeSteps();
private:
    ToolbarView toolbar;
};

#endif // TOOLBARCONTROLLER_H
