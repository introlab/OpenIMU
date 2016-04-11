#include "mainwindow.h"
#include "iostream"
#include <QFileDialog>
#include <QPalette>
#include <qlabel.h>
#include "dateselectorlabel.h"
#include "acquisition/SensorReader.h"
#include "QSplitter"
#include "mytreewidget.h"
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

    splitter->setHandleWidth(30);
    splitter->setSizes(QList<int>() << 150 << 600);
    caneva = new Caneva("../../config/layout1.json", scene);
    tree = new myTreeWidget (this);
    splitter->addWidget(tree);


    //Set QTreeWidget Column Header
    QTreeWidgetItem* headerItem = new QTreeWidgetItem();
    headerItem->setText(0,QString("File Name"));
    tree->setHeaderItem(headerItem);
    tree->setMaximumWidth(150);
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
        /*qDebug() << "List items = " << folderName;
        SensorReader *reader = new SensorReader();
        vector<string> x = reader->listFiles(folderName.toStdString());
        QVBoxLayout *filesLayout = new QVBoxLayout;

        foreach (string t , x){
            DateSelectorLabel* fileName = new DateSelectorLabel(t.c_str());
            filesLayout->addWidget(fileName,0,0);
            connect(fileName, SIGNAL(clicked(std::string)), this, SLOT(onDateSelectedClicked(std::string)));
            }

        */

        QDir* rootDir = new QDir(folderName);
        QFileInfoList filesList = rootDir->entryInfoList();

        foreach(QFileInfo fileInfo, filesList)
        {
          QTreeWidgetItem* item = new QTreeWidgetItem();
          item->setText(0,fileInfo.fileName());

          if(fileInfo.isFile())
          {
            item->setText(1,QString::number(fileInfo.size()));
            item->setIcon(0,*(new QIcon(":/icons/file.png")));
            item->setText(2,fileInfo.filePath());
            tree->addTopLevelItem(item);
          }

          if(fileInfo.isDir() && !fileInfo.fileName().contains("."))
          {
            item->setIcon(0,*(new QIcon(":/icons/folder.png")));
            tree->addChildren(item,fileInfo.filePath());
            item->setText(2,fileInfo.filePath());
            tree->addTopLevelItem(item);
          }

        }
        scene = new CustomQmlScene("layout1.qml", this);
        splitter->addWidget(scene);
        caneva = new Caneva("../../config/layout1.json", scene);
        caneva->setSliderLimitValues(0,10);
        splitter->setSizes(QList<int>() << 150 << 600);
        setCentralWidget(splitter);
}

void MainWindow::onDateSelectedClicked(std::string text){

   }
void MainWindow::onTreeItemClicked(QTreeWidgetItem* item, int column)
{
     caneva->setGraphData(item->text(column).toStdString());
}
void MainWindow:: computeSteps(){
    qDebug()<<"Lance calcul";
}
void MainWindow::closeWindow(){
    this->close();
}
