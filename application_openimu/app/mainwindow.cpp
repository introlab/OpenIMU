#include "mainwindow.h"
#include "iostream"
#include <QFileDialog>
#include "QSplitter"
#include "mytreewidget.h"
#include "accdatadisplay.h"
#include "QMessageBox"

//using namespace std;
QT_CHARTS_USE_NAMESPACE

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
    fileSelectedName = "";
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
    dataView = new QWidget();
    tabWidget->addTab(dataView,"Données accéléromètre");
    splitter->addWidget(tabWidget);
    splitter->setSizes(QList<int>() << 150 << 600);
    setCentralWidget(splitter);
}

MainWindow::~MainWindow(){
    delete splitter;
    delete caneva;
    delete mainWidget;
    delete menu ;
    delete scene;
}

void MainWindow:: openFile(){
    folderName = QFileDialog::getExistingDirectory(this, tr("Ouvrir Fichier"),"/path/to/file/");
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
void MainWindow::onTreeItemClicked(QTreeWidgetItem* item, int column)
{
    if(item->parent()!=NULL){
        fileSelectedName= "/"+item->parent()->text(column)+"/"+item->text(column);
        if(fileSelectedName != "" && fileSelectedName.contains("ACC")){
            std::string reconstructedPath= folderName.toStdString()+"/"+fileSelectedName.toStdString();
            AccDataDisplay *dataDisplay = new AccDataDisplay(reconstructedPath);
            tabWidget->removeTab(0);
              if (dataDisplay->getChartView())
                  tabWidget->insertTab(0, dataDisplay->getChartView(), "Données accéléromètre");

        }
        else{
            QMessageBox msgBox;
            msgBox.setText("Le fichier séléctionné est invalide");
            msgBox.setInformativeText("Choissisez un fichier de type ACC.DAT");
            msgBox.setStandardButtons(QMessageBox::Ok);
            msgBox.exec();
        }
    }
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
