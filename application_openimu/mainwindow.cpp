#include "mainwindow.h"
#include "iostream"
#include <QFileDialog>
using namespace std;

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
    this->setWindowTitle(QString::fromUtf8("Open- IMU"));
    this->setMinimumSize(500,500);
    menu = new ApplicationMenuBar(this);

    mainLayout = new QVBoxLayout;
    mainLayout->setMargin(0);
    mainLayout->addWidget(menu);




    mainWidget = new QWidget;
    mainWidget->setLayout(mainLayout);

    this->setCentralWidget(mainWidget);
}

void MainWindow:: openFile(){
QString fileNames = QFileDialog::getExistingDirectory(this, tr("Open File"),"/path/to/file/");
qDebug() << "List items = " << fileNames;

plotWidget = new Widget(this->parentWidget());
plotWidget->setFolderPath(fileNames.toStdString());
plotWidget->setupPlot();
mainLayout->addWidget(plotWidget);

}
