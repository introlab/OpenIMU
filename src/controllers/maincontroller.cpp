#include "maincontroller.h"
#include "models/displayloader.h"

MainController::MainController(MainWindow& mainWindow)
{
    DisplayLoader loader = DisplayLoader();
    loader.loadLayout(mainWindow);

}
