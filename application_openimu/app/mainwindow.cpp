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
    //this->setStyleSheet("background-color:rgba(216, 222, 219, 0.8);");
    menu = new ApplicationMenuBar(this);
    this->setMenuBar(menu);

    splitter = new QSplitter;
    setCentralWidget(splitter);

    splitter->setHandleWidth(30);
    splitter->handle(1);
    splitter->setSizes(QList<int>() << 150 << 600);
    splitter->setFixedWidth(150);
    tree = new myTreeWidget (this);
    splitter->addWidget(tree);

    //Set QTreeWidget Column Header
    QTreeWidgetItem* headerItem = new QTreeWidgetItem();
    headerItem->setText(0,QString("Explorateur de fichier"));
    tree->setHeaderItem(headerItem);
    tree->setMaximumWidth(150);

    tabWidget = new QTabWidget;
    scene = new CustomQmlScene("displayDataAccelerometer.qml", this);
    tabWidget->addTab(scene,"Données accéléromètre");
    splitter->addWidget(tabWidget);
    caneva = new Caneva("../../config/displayDataAccelerometer.json", scene);
    caneva->setSliderLimitValues(0,10);
    splitter->setSizes(QList<int>() << 150 << 600);
    setCentralWidget(splitter);

   /* scene = new CustomQmlScene("layout1.qml", this);
    splitter->addWidget(scene);
    caneva = new Caneva("../../config/layout1.json", scene);*/
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
        QString folderName = QFileDialog::getExistingDirectory(this, tr("Ouvrir Fichier"),"/path/to/file/");
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
            tree->myTreeWidget::addChildren(item,fileInfo.filePath());
            item->setText(2,fileInfo.filePath());
            tree->addTopLevelItem(item);
          }

        }
}

void MainWindow::onDateSelectedClicked(std::string text){

   }
void MainWindow::onTreeItemClicked(QTreeWidgetItem* item, int column)
{
     caneva->setGraphData(item->text(column).toStdString());
}
void MainWindow:: computeSteps(){
   CustomQmlScene* sceneSteps = new CustomQmlScene("displayStepNumber.qml", this);
    Caneva* canevaSteps = new Caneva("../../config/displayStepNumber.json", sceneSteps);
    tabWidget->addTab(sceneSteps,"Compteur de pas");
}
void MainWindow::computeActivityTime(){
    CustomQmlScene* sceneTime = new CustomQmlScene("displayActivityTime.qml", this);
    Caneva* canevaTime = new Caneva("../../config/displayActivityTime.json", sceneTime);
    tabWidget->addTab(sceneTime,"Temps d'activité");
}
void MainWindow::closeWindow(){
    this->close();
}
