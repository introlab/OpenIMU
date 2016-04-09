#include "mainwindow.h"
#include "iostream"
#include <QFileDialog>
#include <QPalette>
#include <qlabel.h>
#include "dateselectorlabel.h"
#include "acquisition/SensorReader.h"
#include "QSplitter"

using namespace std;

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
    this->setWindowTitle(QString::fromUtf8("Open-IMU"));
    this->setStyleSheet("background: white");
    this->setMinimumSize(700,600);

    menu = new ApplicationMenuBar(this);
    this->setMenuBar(menu);

    splitter = new QSplitter;
    setCentralWidget(splitter);

    QFont f( "Arial", 12, QFont::ExtraLight);
    QLabel * textLabel = new QLabel("Explorateur");
    textLabel->setFont(f);
    mainLayout = new QVBoxLayout;
    mainLayout->addWidget(textLabel);
    filesWidget = new QWidget();
    filesWidget->setMinimumWidth(150);
    filesWidget->setMinimumHeight(580);
    filesWidget->setMaximumWidth(150);
    splitter->addWidget(filesWidget);
    mainLayout->setMargin(0);
    mainLayout->addWidget(filesWidget);
    splitter->setHandleWidth(30);
    splitter->setSizes(QList<int>() << 150 << 600);
}

MainWindow::~MainWindow(){
    delete splitter;
    delete caneva;
    delete mainLayout;
    delete hLayout;
    delete mainWidget;
    delete filesWidget;
    delete menu ;
    delete scene;
}

void MainWindow:: openFile(){
        QString folderName = QFileDialog::getExistingDirectory(this, tr("Open File"),"/path/to/file/");
        qDebug() << "List items = " << folderName;
        SensorReader *reader = new SensorReader();
        vector<string> x = reader->listFiles(folderName.toStdString());
        QVBoxLayout *filesLayout = new QVBoxLayout;
        foreach (string t , x){
            DateSelectorLabel* fileName = new DateSelectorLabel(t.c_str());
            filesLayout->addWidget(fileName,0,0);
            connect(fileName, SIGNAL(clicked(std::string)), this, SLOT(onDateSelectedClicked(std::string)));
            }
        filesWidget->setLayout(filesLayout);
        filesLayout->addStretch();
        scene = new CustomQmlScene("layout1.qml", this);
        splitter->addWidget(scene);
        caneva = new Caneva("../../config/layout1.json", scene);
       // caneva->test();
        caneva->setSliderLimitValues(0,10);
        splitter->setSizes(QList<int>() << 150 << 600);
        setCentralWidget(splitter);
}
void MainWindow::onDateSelectedClicked(std::string text){
    caneva->setGraphData(text);
   }

void MainWindow:: computeSteps(){
    qDebug()<<"Lance calcul";
}
void MainWindow::closeWindow(){
    this->close();
}
