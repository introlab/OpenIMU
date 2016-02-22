#include "builder.h"


Builder::Builder()
{
    displayBuilder = new DisplayBuilder();
}

Display *Builder::load(std::string layoutFile)
{
    this->jsonReader = new JsonReader();
    jsonReader->loadFile(layoutFile);
    this->CreateItems();

    return displayBuilder->GetDisplay();
}

void Builder::CreateItems(){
    for(Json::Value widgetDesc = jsonReader->getNextWidget(); jsonReader->hasWidget(); widgetDesc = jsonReader->getNextWidget())
    {
        std::string widgetName = widgetDesc["widget"].asString();
        int xPos = widgetDesc["pos"]["x"].asInt();
        int yPos = widgetDesc["pos"]["y"].asInt();

        this->controllerList.push_back(this->displayBuilder->CreateWidget(widgetName, xPos, yPos));
    }
}

void Builder::Clear()
{
    this->displayBuilder->Clear();
}
