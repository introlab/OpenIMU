#include "builder.h"


Builder::Builder()
{
    this->jsonReader = new JsonReader();
}

Display *Builder::load(std::string str)
{
    /*
    layoutReader.loadFile("../config/layout1.json");

    for(Json::Value widgetDesc = layoutReader.getNextWidget(); layoutReader.hasWidget(); widgetDesc = layoutReader.getNextWidget())
    {
        std::string widgetName = widgetDesc["widget"].asString();
        int xPos = widgetDesc["pos"]["x"].asInt();
        int yPos = widgetDesc["pos"]["y"].asInt();

        mainWindow.AddCustomWidget(createWidget(widgetName), xPos, yPos);

        std::cout << "name: " << widgetName
                  << " xPos: " << xPos
                  << " yPos: " << yPos
                  << std::endl;
    }
    */
    return new Display();

}
