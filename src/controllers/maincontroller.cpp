#include "maincontroller.h"
#include "models/viewloader.h"

MainController::MainController(MainWindow& mainWindow)
{
    ViewLoader loader = ViewLoader();
    loader.loadLayout(mainWindow);

}
