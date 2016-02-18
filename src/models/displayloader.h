#ifndef DISPLAYLOADER_H
#define DISPLAYLOADER_H

#include "views/mainwindow.h"
#include <QWidget>

class DisplayLoader
{
public:
    DisplayLoader();

    void loadLayout(MainWindow& mainWindow);

private:
    QWidget* createWidget(std::string widgetName);
};

#endif // VIEWLOADER_H
