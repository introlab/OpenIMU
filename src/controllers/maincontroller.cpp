#include "maincontroller.h"

#include "models/builder.h"

MainController::MainController(MainWindow* mainWindow)
{
    std::cout << "Hello";
    this->mainWindow = mainWindow;

    UpdateTab("../config/layout1.json");
    UpdateTab("../config/layout2.json");
    UpdateTab("../config/layout3.json");
    UpdateTab("../config/layout4.json");
    UpdateTab("../config/layout5.json");
}

void MainController::UpdateTab(std::string layoutName)
{
    //TODO
    //if(this->builder != 0) this->builder->Clear();
    Builder* builder = new Builder();
    Display* display = builder->load(layoutName);
    this->mainWindow->explorerDisplay->addTab(display,builder->getDisplayName().c_str());
}

void MainController::AddTab(std::string layoutName)
{
    Builder* builder = new Builder();
    Display* display = builder->load(layoutName);
    this->mainWindow->explorerDisplay->addTab(display,builder->getDisplayName().c_str());
    this->builderList.push_back(builder);
}
