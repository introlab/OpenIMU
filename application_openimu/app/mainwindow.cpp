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
    this->setStyleSheet("background: rgba(246, 254, 254,0.8)");
    this->setMinimumSize(700,600);
    menu = new ApplicationMenuBar(this);
    this->setMenuBar(menu);
    statusBar = new QStatusBar();
    this->setStatusBar(statusBar);
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

    //default scene
    //scene = new CustomQmlScene("test_slider_chart.qml", this);
    //caneva = new Caneva("../../config/test_slider_chart.json", scene);
    tabWidget = new QTabWidget;
    //tabWidget->addTab(scene,"Test slider with chart");
    tabWidget->setTabsClosable(true);
    connect(tabWidget, SIGNAL(tabCloseRequested(int)), this, SLOT(closeTab(int)));
    dataView = new QWidget();
    tabWidget->addTab(dataView,"Données accéléromètre");
    tabWidget->tabBar()->tabButton(0, QTabBar::RightSide)->hide();
    tabWidget->setCurrentWidget(tabWidget->widget(0));
    splitter->addWidget(tabWidget);
    splitter->setSizes(QList<int>() << 150 << 600);
    setCentralWidget(splitter);
    statusBar->showMessage(tr("Prêt"));
   // caneva->test_slider_chart();
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
    statusBar->showMessage(QString::fromStdString("Dossier séléctionné: ")+ folderName);
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
        QString status = QString::fromStdString("Fichier séléctionné: ") + fileSelectedName;
        statusBar->showMessage(status);
        if(fileSelectedName != "" && fileSelectedName.contains("ACC")){
            std::string reconstructedPath= folderName.toStdString()+"/"+fileSelectedName.toStdString();
            AccDataDisplay *dataDisplay = new AccDataDisplay(reconstructedPath);
            replaceTab(dataDisplay,"Données accéléromètre");
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
    replaceTab(sceneSteps,"Compteur de pas");
    canevaSteps->testSteps();
    statusBar->showMessage(tr("Ouverture compteur de pas"));
}
void MainWindow::computeActivityTime(){
    CustomQmlScene* sceneTime = new CustomQmlScene("displayActivityTime.qml", this);
    Caneva* canevaTime = new Caneva("../../config/displayActivityTime.json", sceneTime);
    replaceTab(sceneTime,"Temps d'activité");
    canevaTime->testActivity();
    statusBar->showMessage(tr("Ouverture temps d'activité"));

}
void MainWindow::openAbout(){

    aboutDialog = new AboutDialog(this);
    aboutDialog->exec();
}

void MainWindow::openHelp(){
    helpDialog = new HelpDialog(this);
    helpDialog->exec();
}

void MainWindow::replaceTab(QWidget * replacement, std::string label)
{
    int index = 0;
    bool found  = false;
    QString currentTabText;

    for(int i=0; i<tabWidget->count();i++){
        currentTabText = tabWidget->tabText(i);
        if(currentTabText == QString::fromStdString(label)){
            index = i;
            found = true;
        }
    }
    if(found){
        tabWidget->removeTab(index);
        if (replacement){
            tabWidget->insertTab(index, replacement, QString::fromStdString(label));
            tabWidget->setCurrentWidget(tabWidget->widget(index));
        }
    }
    else
    {
        tabWidget->addTab(replacement,QString::fromStdString(label));
        tabWidget->setCurrentWidget(tabWidget->widget(tabWidget->count()-1));
    }
}
void MainWindow::closeTab(int index){

    if (index == -1) {
        return;
    }
    QWidget* tabItem = tabWidget->widget(index);
    // Removes the tab at position index from this stack of widgets.
    // The page widget itself is not deleted.
    tabWidget->removeTab(index);

    delete(tabItem);
    tabItem = nullptr;
}
void MainWindow::closeWindow(){
    this->close();
}
