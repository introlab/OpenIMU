#ifndef MAINCONTROLLER_H
#define MAINCONTROLLER_H

#include "views/mainwindow.h"
#include "models/builder.h"

class MainController
{
public:
    MainController(MainWindow* mainWindow);
private:
    void UpdateTab(std::string layoutName);
    MainWindow* mainWindow;
    Builder* builder;
};

#endif // MAINCONTROLLER_H
