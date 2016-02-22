#include "maincontroller.h"

#include "models/builder.h"

MainController::MainController(MainWindow* mainWindow)
{
    std::cout << "Hello";
    this->mainWindow = mainWindow;

    this->mainWindow->explorerDisplay->addTab(new QWidget(),"Dummy");

    UpdateTab("../config/layout1.json");
}

void MainController::UpdateTab(std::string layoutName)
{
    //if(this->builder != 0) this->builder->Clear();
    this->builder = new Builder();
    this->mainWindow->explorerDisplay->addTab(builder->load(layoutName),"layout1");
}
