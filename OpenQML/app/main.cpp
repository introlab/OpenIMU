#include "mainwindow.h"
#include <QApplication>
#include <QtQuick/QtQuick>


int main(int argc, char *argv[])
{

    QApplication a(argc, argv);
    MainWindow w;

    w.show();

    //QQmlApplicationEngine appEngine;
    //appEngine.load(QUrl(QStringLiteral("qrc:/main.qml")));

    return a.exec();
}
