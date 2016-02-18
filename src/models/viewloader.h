#ifndef VIEWLOADER_H
#define VIEWLOADER_H

#include "views/mainwindow.h"
#include <QWidget>

class ViewLoader
{
public:
    ViewLoader();

    void loadLayout(MainWindow& mainWindow);

private:
    QWidget* createWidget(std::string widgetName);
};

#endif // VIEWLOADER_H
