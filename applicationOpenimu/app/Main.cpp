#include <QApplication>
#include <QMainWindow>
#include "MainWindow.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    QString locale = QLocale::system().name();

    QTranslator translator;
    if(translator.load(QString("../translations/openImu_") + locale))
    {
           qDebug() << QString("../translations/openImu_") + locale << " loaded";
    }
    else
    {
           qDebug() <<QString("../translations/openImu_") + locale << "loading failed";
    }
    a.installTranslator(&translator);

    MainWindow *window = new MainWindow();
    window->show();

    return a.exec();
}



