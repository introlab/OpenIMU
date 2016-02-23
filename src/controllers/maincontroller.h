#ifndef MAINCONTROLLER_H
#define MAINCONTROLLER_H

#include "views/mainwindow.h"
#include "models/builder.h"
#include <list>

class MainController
{
public:
    MainController(MainWindow* mainWindow);
private:
    void UpdateTab(std::string layoutName);
    void AddTab(std::string layoutName);
    MainWindow* mainWindow;
    std::list<Builder*> builderList;
};

#endif // MAINCONTROLLER_H
