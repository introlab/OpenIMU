#include <QFileDialog>
#include "QTableView"
#include <QListWidgetItem>
#include<vector>
#include<QDebug>
#include "widgets/AlgorithmTab.h"
#include "widgets/ResultsTabWidget.h"
#include "AccDataDisplay.h"
#include "QMessageBox"
#include "mainwindow.h"
#include "iostream"
#include <QtConcurrent/QtConcurrentRun>

QT_CHARTS_USE_NAMESPACE

const QString frenchText = "French";
const QString englishText = "English";

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
    this->grabGesture(Qt::PanGesture);
    this->grabGesture(Qt::PinchGesture);

    this->setWindowTitle(QString::fromUtf8("Open-IMU"));
    this->setStyleSheet("background: rgba(246, 254, 254,0.8)");
    this->setMinimumSize(900,700);

    menu = new ApplicationMenuBar(this);
    statusBar = new QStatusBar();
    mainWidget = new MainWidget(this);
    listWidget = new MyListWidget(this);
    tabWidget = new QTabWidget;
    spinnerStatusBar = new QLabel;
    movieSpinnerBar = new QMovie("../applicationOpenimu/app/icons/loaderStatusBar.gif");

    spinnerStatusBar->setMovie(movieSpinnerBar);
    connect(tabWidget, SIGNAL(tabCloseRequested(int)), this, SLOT(closeTab(int)));
    connect(listWidget, SIGNAL(itemClicked(QListWidgetItem*)),this, SLOT(onListItemClicked(QListWidgetItem*)));

    this->setMenuBar(menu);
    this->setStatusBar(statusBar);

    statusBar->setStyleSheet("background-color:rgba(230, 233, 239,0.2);");
    listWidget->setAlternatingRowColors(true);
    listWidget->setStyleSheet("alternate-background-color:#ecf0f1;background-color:white;");

    mainWidget->mainLayout->addWidget(listWidget);

    listWidget->setMaximumWidth(150);
    tabWidget->setTabsClosable(true);
    homeWidget = new HomeWidget(this);

    tabWidget->addTab(homeWidget,tr("Accueil"));
    tabWidget->setStyleSheet("background: rgb(247, 250, 255,0.6)");
    tabWidget->setCurrentWidget(tabWidget->widget(0));
    tabWidget->grabGesture(Qt::PanGesture);
    tabWidget->grabGesture(Qt::PinchGesture);
    mainWidget->mainLayout->addWidget(tabWidget);

    setCentralWidget(mainWidget);
    statusBar->showMessage(tr("Prêt"));
    statusBar->addPermanentWidget(spinnerStatusBar);

    //Execute launchApi in a thread
    future = new QFuture<void>;
    watcher = new QFutureWatcher<void>;
    *future = QtConcurrent::run(MainWindow::launchApi);
    watcher->setFuture(*future);

    getRecordsFromDB();

}

MainWindow::~MainWindow(){
    delete menu ;
}

void MainWindow::onListItemClicked(QListWidgetItem* item)
{
    for(int i=0; i<record.m_WimuRecordList.size();i++)
    {
        if(record.m_WimuRecordList.at(i).m_recordName.compare(item->text().toStdString()) == 0)
        {
            statusBar->showMessage(tr("Chargement..."));
            selectedUUID = record.m_WimuRecordList.at(i).m_recordId;
            spinnerStatusBar->show();
            movieSpinnerBar->start();
            getDataFromUUIDFromDB(selectedUUID);
            recordsTab = new RecordsWidget(this,acceleroData,record.m_WimuRecordList.at(i));
            replaceTab(recordsTab,"Informations enregistrement");
            movieSpinnerBar->stop();
            spinnerStatusBar->hide();
            statusBar->showMessage(tr("Prêt"));

        }
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

void MainWindow::openAlgorithmTab()
{
    algorithmTab = new AlgorithmTab(this,selectedUUID);
    replaceTab(algorithmTab,"Algorithmes");
}

void MainWindow::deleteRecord()
{
    QMessageBox msgBox;
    msgBox.setText("Suppression de l'enregistrement");
    msgBox.setInformativeText("Êtes vous sûr de vouloir supprimer cet enregistrement?");
    msgBox.setStandardButtons(QMessageBox::Ok | QMessageBox::Cancel);
    msgBox.setDefaultButton(QMessageBox::Cancel);
    int ret = msgBox.exec();

    switch (ret) {
      case QMessageBox::Ok:
        deleteRecordFromUUID(selectedUUID);
        getRecordsFromDB();
        acceleroData.clearData();
        selectedUUID= "";
        tabWidget->removeTab(tabWidget->currentIndex());
        openHomeTab();
          break;
      case QMessageBox::Cancel:
          // Cancel was clicked
          break;
      default:
          // should never be reached
          break;
    }

}

void MainWindow::openHomeTab()
{
    homeWidget = new HomeWidget(this);
    replaceTab(homeWidget,"Accueil");
}

bool MainWindow::getRecordsFromDB()
{
    QNetworkRequest request(QUrl("http://127.0.0.1:5000/records"));
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QNetworkReply *reply = manager->get(request);
    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), this ,SLOT(reponseRecue(QNetworkReply*)));

    return true;
}

bool MainWindow::getDataFromUUIDFromDB(std::string uuid)
{
    std::string url = "http://127.0.0.1:5000/data?uuid="+uuid;
    QNetworkRequest request(QUrl(QString::fromStdString(url)));
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QNetworkReply *reply = manager->get(request);
    QEventLoop loop;
    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), &loop,SLOT(quit()));
    loop.exec();
    reponseRecueAcc(reply);
    return true;
}

void MainWindow::reponseRecueAcc(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
   {
       acceleroData.clearData();
       std::string testReponse(reply->readAll());
       CJsonSerializer::Deserialize(&acceleroData, testReponse);

   }
   else
   {
       //qDebug() << "error connect";
       //qWarning() <<"ErrorNo: "<< reply->error() << "for url: " << reply->url().toString();
       //qDebug() << "Request failed, " << reply->errorString();
      // qDebug() << "Headers:"<<  reply->rawHeaderList()<< "content:" << reply->readAll();
       //qDebug() << reply->readAll();
   }
   delete reply;
}

void MainWindow::reponseRecue(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
   {
       std::string testReponse(reply->readAll());
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
       //qDebug() << "error connect";
       //qWarning() <<"ErrorNo: "<< reply->error() << "for url: " << reply->url().toString();
       //qDebug() << "Request failed, " << reply->errorString();
       //qDebug() << "Headers:"<<  reply->rawHeaderList()<< "content:" << reply->readAll();
       //qDebug() << reply->readAll();
   }
   delete reply;
}

//Delete specific record
bool MainWindow::deleteRecordFromUUID(std::string uuid)
{
    std::string url = "http://127.0.0.1:5000/delete?uuid="+uuid;
    QNetworkRequest request(QUrl(QString::fromStdString(url)));
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QNetworkReply *reply = manager->get(request);
    QEventLoop loop;
    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), &loop,SLOT(quit()));
    loop.exec();
    reponseRecueDelete(reply);
    return true;
}

void MainWindow::reponseRecueDelete(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
   {
        statusBar->showMessage(tr("Enregistrement effacé avec succès"));
   }
   else
   {
        statusBar->showMessage(tr("Echec de suppression de l'enregistrement"));
   }
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
