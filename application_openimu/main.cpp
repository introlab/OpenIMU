#include "widget.h"
#include <QApplication>
#include <QMainWindow>
#include <QMenuBar>
#include <QVBoxLayout>
#include "applicationmenubar.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    QMainWindow *window = new QMainWindow();
    QWidget *mainWidget = new QWidget;
    window->setWindowTitle(QString::fromUtf8("Open- IMU"));

    Widget *plotWidget = new Widget(window);
    ApplicationMenuBar* menu = new ApplicationMenuBar(window);

    QVBoxLayout *mainLayout = new QVBoxLayout;
    mainLayout->setMargin(0);
    mainLayout->addWidget(menu);
    mainLayout->addWidget(plotWidget);
    mainWidget->setLayout(mainLayout);

    window->setCentralWidget(mainWidget);
    window->show();

    return a.exec();
}
