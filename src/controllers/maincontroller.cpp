#include "maincontroller.h"
#include "models/displayloader.h"

#include "models/builder.h"

MainController::MainController(MainWindow* mainWindow)
{
    std::cout << "Hello";
    this->mainWindow = mainWindow;
    this->displayBuilder = new Builder();
    this->mainWindow->explorerDisplay->addTab(new QWidget(),"Dummy");

    //DisplayLoader loader = DisplayLoader();
    //loader.loadLayout(mainWindow);

}

void MainController::AddTab(std::string layoutName)
{
    this->mainWindow->explorerDisplay->addTab(new QWidget(),"Dummy");
}
