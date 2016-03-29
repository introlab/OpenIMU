#include "mainwindow.h"
#include "iostream"
#include <QFileDialog>
#include <QPalette>
#include <qlabel.h>
#include "dateselectorlabel.h"
#include "acquisition/SensorReader.h"

using namespace std;

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
    this->setWindowTitle(QString::fromUtf8("Open-IMU"));
    this->setMinimumSize(500,500);
    menu = new ApplicationMenuBar(this);
    menu->setMaximumHeight(20);
    filesWidget = new QWidget();
    QPalette Pal(palette());

    // set black background
    Pal.setColor(QPalette::Background, Qt::white);
    filesWidget->setAutoFillBackground(true);
    filesWidget->setMaximumWidth(200);
    filesWidget->setPalette(Pal);
    filesWidget->setStyleSheet("border: 1px solid red");
    mainLayout = new QVBoxLayout;
    mainLayout->setMargin(0);
    mainLayout->addWidget(menu);
    QFont f( "Arial", 12, QFont::ExtraLight);
    QLabel * textLabel = new QLabel("Explorateur");
    textLabel->setFont(f);
    mainLayout->addWidget(textLabel);
    mainLayout->addWidget(filesWidget);
    mainWidget = new QWidget;
    mainWidget->setLayout(mainLayout);

    this->setCentralWidget(mainWidget);
}

string MainWindow::getFileName(string s){
    char sep = '/';
    size_t i = s.rfind(sep, s.length());
    if (i != string::npos) {
       return(s.substr(i+1, s.length() - i));
    }

    return("");
}

void MainWindow:: openFile(){
        QString folderName = QFileDialog::getExistingDirectory(this, tr("Open File"),"/path/to/file/");
        qDebug() << "List items = " << folderName;
        SensorReader *reader = new SensorReader();
        vector<string> x = reader->listFiles(folderName.toStdString());
        QVBoxLayout *filesLayout = new QVBoxLayout;

        foreach (string t , x){
            DateSelectorLabel* fileName = new DateSelectorLabel(getFileName(t).c_str());
            filesLayout->addWidget(fileName,0,0);
            connect(fileName, SIGNAL(clicked(std::string)), this, SLOT(computeSteps(std::string)));
        }
        filesWidget->setLayout(filesLayout);
}
void MainWindow:: computeSteps(std::string text){
    qDebug() << "here"<<text.c_str();
   /* plotWidget = new Widget(this->parentWidget());
    plotWidget->setFolderPath(text);
    plotWidget->setupPlot();
    mainLayout->addWidget(plotWidget);*/
}
