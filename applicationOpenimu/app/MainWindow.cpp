#include "mainwindow.h"
#include "iostream"
#include <QFileDialog>
#include "QSplitter"
#include "AccDataDisplay.h"
#include "QMessageBox"
#include <QListWidgetItem>
#include<vector>
#include<QDebug>

QT_CHARTS_USE_NAMESPACE

const QString frenchText = "French";
const QString englishText = "English";

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
    fileSelectedName = "";

    this->grabGesture(Qt::PanGesture);
    this->grabGesture(Qt::PinchGesture);

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

    listWidget = new MyListWidget(this);
    connect(listWidget, SIGNAL(itemClicked(QListWidgetItem*)),this, SLOT(onListItemClicked(QListWidgetItem*)));

    listWidget->setAlternatingRowColors(true);
    listWidget->setStyleSheet("alternate-background-color:#ecf0f1;background-color:#white;");

    //Implementation listWidget for days in dB
   //  splitter->addWidget(populateDaysFromDataBase());
    splitter->addWidget(listWidget);

    QListWidgetItem *headerItem  = new QListWidgetItem();
    headerItem->setText(QString(tr("Enregistrements")));
    listWidget->addItem(headerItem);
    listWidget->setMaximumWidth(150);
    tabWidget = new QTabWidget;
    tabWidget->setTabsClosable(true);
    connect(tabWidget, SIGNAL(tabCloseRequested(int)), this, SLOT(closeTab(int)));
    QWidget * homeWidget = new QWidget(); //To do create classe Home widget
    QFont font;
    font.setPointSize(14);
    font.setBold(true);
    QVBoxLayout* homeLayout = new QVBoxLayout(homeWidget);
    QLabel * homeLabel = new QLabel("Open IMU");
    QLabel * descriptionLabel = new QLabel(tr("Logiciel de visualisation et d'analyse, Open Source"));
    QLabel * descriptionLabel2 = new QLabel(tr("pour centrale inertielle"));
    homeLabel->setFont(font);
    descriptionLabel->setFont(font);
    descriptionLabel2->setFont(font);
    homeLayout->addWidget(homeLabel);
    homeLayout->addWidget(descriptionLabel);
    homeLayout->addWidget(descriptionLabel2);
    homeLayout -> setAlignment(homeLabel,Qt::AlignCenter);
    homeLayout -> setAlignment(descriptionLabel,Qt::AlignCenter);
    homeLayout -> setAlignment(descriptionLabel2,Qt::AlignCenter);
    homeWidget->setLayout(homeLayout);
    tabWidget->addTab(homeWidget,tr("Accueil"));

    qDebug() << tabWidget->tabBar();
    qDebug() << tabWidget->tabBar()->tabButton(0,QTabBar::RightSide);

    tabWidget->setCurrentWidget(tabWidget->widget(0));
    tabWidget->grabGesture(Qt::PanGesture);
    tabWidget->grabGesture(Qt::PinchGesture);
    splitter->addWidget(tabWidget);
    splitter->setSizes(QList<int>() << 150 << 600);
    setCentralWidget(splitter);
    statusBar->showMessage(tr("Prêt"));
    getRecordsFromDB();
}

MainWindow::~MainWindow(){
    delete splitter;
    delete caneva;
    delete mainWidget;
    delete menu ;
    delete scene;
}

void MainWindow::onListItemClicked(QListWidgetItem* item)
{
    for(int i=0; i<record.m_WimuRecordList.size();i++)
    {
        if(record.m_WimuRecordList.at(i).m_recordName.compare(item->text().toStdString()) == 0)
        {
            AccDataDisplay *dataDisplay = new AccDataDisplay(record.m_WimuRecordList.at(i).m_recordId);// C://Users//stef//Desktop//Projet S7-S8//data_step//10//ACC_4.DAT");
            QString dataAcc = tr("Données accéléromètre");
            std::string sDataAcc = dataAcc.toUtf8().constData();
            replaceTab(dataDisplay, sDataAcc);
        }
    }
}

QListWidget* MainWindow::populateDaysFromDataBase()
{
    QListWidget* listWidget = new QListWidget(this);
    for(QString day: databaseAccess->getDaysInDB())
    {
        QListWidgetItem *newItem = new QListWidgetItem;
        newItem->setText(day);
        listWidget->insertItem(listWidget->count(), newItem);
    }
    connect(listWidget, SIGNAL(itemClicked(QListWidgetItem *)), SLOT(dateClicked(QListWidgetItem *)));
    return listWidget;
}

void MainWindow::dateClicked(QListWidgetItem *item)
{
    if(item)
    {
        statusBar->showMessage(item->text());
    }
}

void MainWindow:: openFile(){
    getRecordsFromDB();
}

void MainWindow:: openRecordDialog()
{
    rDialog = new RecordsDialog;
    rDialog->show();
}

void MainWindow::onTreeItemClicked(QTreeWidgetItem* item, int column)
{
    if(item->parent()!=NULL){
        fileSelectedName= "/"+item->parent()->text(column)+"/"+item->text(column);
    }
    else{
        fileSelectedName = item->text(column);
    }
    QString status = tr("Fichier séléctionné: ") + fileSelectedName;
    statusBar->showMessage(status);
    if(fileSelectedName != "" && fileSelectedName.contains("ACC")){
        std::string reconstructedPath= folderName.toStdString()+"/"+fileSelectedName.toStdString();
        AccDataDisplay *dataDisplay = new AccDataDisplay(reconstructedPath);
        QString dataAcc = tr("Données accéléromètre");
        std::string sDataAcc = dataAcc.toUtf8().constData();
        replaceTab(dataDisplay, sDataAcc);
    }
    else{
        QMessageBox msgBox;
        msgBox.setText(tr("Le fichier séléctionné est invalide"));
        msgBox.setInformativeText(tr("Choissisez un fichier de type ACC.DAT"));
        msgBox.setStandardButtons(QMessageBox::Ok);
        msgBox.exec();
    }

}
void MainWindow:: displayRawAccData()
{
    if(fileSelectedName != "" && fileSelectedName.contains("ACC")){
        std::string reconstructedPath= folderName.toStdString()+"/"+fileSelectedName.toStdString();
        AccDataDisplay *dataDisplay = new AccDataDisplay(reconstructedPath);
        QString dataAcc = tr("Données accéléromètre");
        std::string sDataAcc = dataAcc.toUtf8().constData();
        replaceTab(dataDisplay,sDataAcc);
    }
    else{
        QMessageBox msgBox;
        msgBox.setText(tr("Le fichier séléctionné est invalide"));
        msgBox.setInformativeText(tr("Choissisez un fichier de type ACC.DAT"));
        msgBox.setStandardButtons(QMessageBox::Ok);
        msgBox.exec();
    }
}
void MainWindow:: computeSteps(){
    std::string reconsrtructPath = folderName.toStdString()+"/"+fileSelectedName.toStdString();
    if(reconsrtructPath != "/" ){
        CustomQmlScene* sceneSteps = new CustomQmlScene("displayStepNumber.qml", this);
        Caneva* canevaSteps = new Caneva("config/displayStepNumber.json", sceneSteps);
        QString stepCount = tr("Compteur de pas");
        std::string sStepCount = stepCount.toUtf8().constData();
        replaceTab(sceneSteps,sStepCount);
        canevaSteps->testSteps(reconsrtructPath);
        statusBar->showMessage(tr("Ouverture compteur de pas"));
    }
    else{
        QMessageBox msgBox;
        msgBox.setText(tr("Pas de fichier séléctionné"));
        msgBox.setInformativeText(tr("Choissisez un fichier de type ACC.DAT"));
        msgBox.setStandardButtons(QMessageBox::Ok);
        msgBox.exec();
    }
}
void MainWindow::computeActivityTime(){
    if(selectedUUID != ""){
        CustomQmlScene* sceneTime = new CustomQmlScene("displayActivityTime.qml", this);
        Caneva* canevaTime = new Caneva("config/displayActivityTime.json", sceneTime);
        QString actTime = tr("Temps d'activité");
        std::string sActTime = actTime.toUtf8().constData();
        replaceTab(sceneTime,sActTime);
        canevaTime->testActivity(selectedUUID);
    }
    else{
        QMessageBox msgBox;
        msgBox.setText(tr("Pas de fichier séléctionné"));
        msgBox.setInformativeText(tr("Choissisez un fichier de type ACC.DAT"));
        msgBox.setStandardButtons(QMessageBox::Ok);
        msgBox.exec();
    }

    statusBar->showMessage(tr("Ouverture temps d'activité"));

}

void MainWindow::setApplicationInEnglish()
{
    menu->setUncheck(frenchText);
    //TODO: Olivier, insert change language logic here
}

void MainWindow::setApplicationInFrench()
{
    menu->setUncheck(englishText);
    //TODO: Olivier, insert change language logic here
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
        if(currentTabText == tr("Accueil")){
            tabWidget->removeTab(i);
        }
    }
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

bool MainWindow::getRecordsFromDB()
{
    QNetworkRequest request(QUrl("http://127.0.0.1:5000/records"));
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QNetworkReply *reply = manager->get(request);
    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), this,SLOT(reponseRecue(QNetworkReply*)));

    return true;
}

void MainWindow::reponseRecue(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
   {
       qDebug() << "connection main";
       std::string testReponse = reply->readAll();
       record.m_WimuRecordList.clear();
       CJsonSerializer::Deserialize(&record, testReponse);

       listWidget->clear();
       for(int i=0; i<record.m_WimuRecordList.size();i++)
       {
           listWidget->addItem(QString::fromStdString(record.m_WimuRecordList.at(i).m_recordName));
       }
   }
   else
   {
       qDebug() << "error connect";
       qWarning() <<"ErrorNo: "<< reply->error() << "for url: " << reply->url().toString();
       qDebug() << "Request failed, " << reply->errorString();
       qDebug() << "Headers:"<<  reply->rawHeaderList()<< "content:" << reply->readAll();
       qDebug() << reply->readAll();
   }
   delete reply;
}
