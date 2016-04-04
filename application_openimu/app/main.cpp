#include "widget.h"
#include <QApplication>
#include <QMainWindow>
#include <QMenuBar>
#include <QVBoxLayout>
#include "applicationmenubar.h"
#include "mainwindow.h"

int main(int argc, char *argv[])
{
    //Caneva caneva("../config/layout1.json");
    QApplication a(argc, argv);

    MainWindow *window = new MainWindow();
    window->show();

    return a.exec();
}
