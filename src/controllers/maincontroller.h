#ifndef MAINCONTROLLER_H
#define MAINCONTROLLER_H

#include "views/mainwindow.h"
#include "models/builder.h"

class MainController
{
public:
    MainController(MainWindow* mainWindow);
private:
    MainWindow* mainWindow;
    Builder* displayBuilder;
};

#endif // MAINCONTROLLER_H