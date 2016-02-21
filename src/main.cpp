#include "views/mainwindow.h"
#include <QApplication>
#include "models/displayloader.h"
#include "controllers/maincontroller.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    //MainController mainController(w);
    w.show();

    return a.exec();
}
