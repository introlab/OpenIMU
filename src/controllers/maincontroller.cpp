#include "maincontroller.h"
#include "models/displayloader.h"

MainController::MainController(MainWindow* mainWindow)
{
    std::cout << "Hello";
    this->mainWindow = mainWindow;
    this->displayBuilder = new DisplayBuilder();
    this->mainWindow->explorerDisplay->addTab(new QWidget(),"Dummy");

    //DisplayLoader loader = DisplayLoader();
    //loader.loadLayout(mainWindow);

}
