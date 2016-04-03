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
    test=false;
    this->setWindowTitle(QString::fromUtf8("Open-IMU"));
    plotWidget = new Widget();
    plotWidget->setVisible(false);
    this->setMinimumSize(700,600);
    menu = new ApplicationMenuBar(this);
    menu->setMaximumHeight(20);
    filesWidget = new QWidget();
    QPalette Pal(palette());

    filesWidget->setMinimumWidth(150);
    filesWidget->setMinimumHeight(580);
    filesWidget->setMaximumWidth(200);

    hLayout = new QHBoxLayout;
    hLayout->addWidget(filesWidget);
    hLayout->addStretch();

    mainLayout = new QVBoxLayout;
    mainLayout->setMargin(0);
    mainLayout->addWidget(menu);
    QFont f( "Arial", 12, QFont::ExtraLight);
    QLabel * textLabel = new QLabel("Explorateur");
    textLabel->setFont(f);
    mainLayout->addWidget(textLabel);
    mainLayout->addLayout(hLayout);
    mainLayout->addStretch();
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
// To do: better handling, remove this part
        filesWidget = new QWidget();
        filesWidget->setMinimumWidth(150);
        filesWidget->setMinimumHeight(580);
        filesWidget->setMaximumWidth(200);
        filesWidget->setStyleSheet( "border-radius: 5px; "
                                     "border: 1px solid black;"
                                   );
        hLayout = new QHBoxLayout;
        hLayout->addWidget(filesWidget);
        hLayout->addStretch();

        mainWidget = new QWidget;
        mainLayout = new QVBoxLayout(mainWidget);
        mainLayout->setMargin(0);
        mainLayout->addWidget(menu);
        QFont f( "Arial", 12, QFont::ExtraLight);
        QLabel * textLabel = new QLabel("Explorateur");
        textLabel->setFont(f);
        mainLayout->addWidget(textLabel);
        mainLayout->addLayout(hLayout);
        mainLayout->addStretch();
//************
        foreach (string t , x){
            DateSelectorLabel* fileName = new DateSelectorLabel(t.c_str());
            filesLayout->addWidget(fileName,0,0);
            connect(fileName, SIGNAL(clicked(std::string)), this, SLOT(onDateSelectedClicked(std::string)));
            }

        filesWidget->setLayout(filesLayout);
        filesLayout->addStretch();
        hLayout->addWidget(plotWidget);
        hLayout->addStretch();
        this->setCentralWidget(mainWidget);
}
void MainWindow::onDateSelectedClicked(std::string text){
    plotWidget->setFolderPath(text);
    plotWidget->setupPlot();
    plotWidget->setVisible(true);

   }

void MainWindow:: computeSteps(){

}
