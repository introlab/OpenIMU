#ifndef MAINCONTROLLER_H
#define MAINCONTROLLER_H

#include "views/mainwindow.h"
#include "models/displaybuilder.h"

class MainController
{
public:
    MainController(MainWindow* mainWindow);
private:
    MainWindow* mainWindow;
    DisplayBuilder* displayBuilder;
};

#endif // MAINCONTROLLER_H
