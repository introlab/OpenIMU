#include <QFileDialog>
#include "QTableView"
#include <QListWidgetItem>
#include<vector>
#include<QDebug>

#include "AccDataDisplay.h"
#include "QMessageBox"
#include "mainwindow.h"
#include "iostream"

QT_CHARTS_USE_NAMESPACE

const QString frenchText = "French";
const QString englishText = "English";

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
    this->grabGesture(Qt::PanGesture);
    this->grabGesture(Qt::PinchGesture);

    this->setWindowTitle(QString::fromUtf8("Open-IMU"));
    this->setStyleSheet("background: rgba(246, 254, 254,0.8)");
    this->setMinimumSize(700,600);

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
    tabWidget->setStyleSheet("background-color:white;");
    QWidget * homeWidget = new QWidget(); //To do create classe Home widget
    QVBoxLayout* homeLayout = new QVBoxLayout(homeWidget);
    QLabel * homeLabel = new QLabel("Open IMU,logiciel de visualisation et d'analyse pour centrale inertielle");

    QPixmap pic("../applicationOpenimu/app/icons/logo.png");
    QPixmap scaled=pic.scaled ( 400, 200, Qt::KeepAspectRatio, Qt::FastTransformation );

    QLabel *label = new QLabel(this);
    label->setMaximumWidth(800);
    label->setPixmap(scaled);
    label->setAlignment(Qt::AlignCenter);
    QFont font;
    font.setPointSize(10);
    homeLabel->setFont(font);

    homeLayout->addWidget(homeLabel);
    homeWidget->setLayout(homeLayout);
    homeLayout->addWidget(label);
    homeLayout->addSpacing(100);
    homeLayout -> setAlignment(homeLabel,Qt::AlignCenter);
    tabWidget->addTab(homeWidget,tr("Accueil"));
/*
    // -- Algorithm Tab -- TODO: MOVE BY MADO
    QWidget * algorithmWidget = new QWidget(); //To do create classe Home widget
    QVBoxLayout* algorithmLayout = new QVBoxLayout(algorithmWidget);

    // -- Algorithm Section
    QLabel *algorithmLabel = new QLabel(tr("Algorithms"));

    QTableView *algorithmTableView = new QTableView(this);
   // connect(algorithmTableView, SIGNAL(itemClicked(QTableViewItem*)),this, SLOT(onListItemClicked(QTableViewItem*)));

    //algorithmTableView->setAlternatingRowColors(true);
    //algorithmTableView->setStyleSheet("alternate-background-color:#ecf0f1;background-color:white;");

    QStandardItemModel *algorithmModel = new QStandardItemModel(this);
    algorithmModel->setHeaderData(0, Qt::Horizontal, QObject::tr("ID"));
    algorithmModel->setHeaderData(1, Qt::Horizontal, QObject::tr("Name"));
    algorithmModel->setHeaderData(2, Qt::Horizontal, QObject::tr("Description"));
    algorithmModel->setHeaderData(3, Qt::Horizontal, QObject::tr("Author"));

    algorithmTableView->setModel(algorithmModel);
    algorithmTableView->show();

    // -- Parameter Section
    QLabel *parameterLabel = new QLabel(tr("Parameter(s)"));

    algorithmLayout->addWidget(algorithmLabel);
    algorithmLayout->addWidget(algorithmTableView);
    algorithmLayout->addWidget(parameterLabel);
    algorithmWidget->setLayout(algorithmLayout);

    tabWidget->addTab(algorithmWidget,tr("Algorithmes"));

    // -- END OF Algorithm Tab -- TODO: MOVE BY MADO

*/
    tabWidget->setCurrentWidget(tabWidget->widget(0));
    tabWidget->grabGesture(Qt::PanGesture);
    tabWidget->grabGesture(Qt::PinchGesture);
    mainWidget->mainLayout->addWidget(tabWidget);
    setCentralWidget(mainWidget);
    statusBar->showMessage(tr("Prêt"));
    statusBar->addPermanentWidget(spinnerStatusBar);
    getRecordsFromDB();
}

MainWindow::~MainWindow(){
    delete caneva;
    delete menu ;
    delete scene;
}

void MainWindow::onListItemClicked(QListWidgetItem* item)
{
    for(int i=0; i<record.m_WimuRecordList.size();i++)
    {
        if(record.m_WimuRecordList.at(i).m_recordName.compare(item->text().toStdString()) == 0)
        {
            selectedUUID = record.m_WimuRecordList.at(i).m_recordId;
            spinnerStatusBar->show();
            movieSpinnerBar->start();
            getDataFromUUIDFromDB(selectedUUID);
            recordsTab = new RecordsWidget(this,acceleroData,record.m_WimuRecordList.at(i));
            QString recordInfo = tr("Informations enregistrement");
            std::string srecordInfo = recordInfo.toUtf8().constData();
            replaceTab(recordsTab, srecordInfo);
            movieSpinnerBar->stop();
            spinnerStatusBar->hide();
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
       qDebug() << "connection UUID";
       std::string testReponse(reply->readAll());
       CJsonSerializer::Deserialize(&acceleroData, testReponse);

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

void MainWindow:: computeSteps(){
        CustomQmlScene* sceneSteps = new CustomQmlScene("displayStepNumber.qml", this);
        Caneva* canevaSteps = new Caneva("config/displayStepNumber.json", sceneSteps);
        QString stepCount = tr("Compteur de pas");
        std::string sStepCount = stepCount.toUtf8().constData();
        replaceTab(sceneSteps,sStepCount);
        getDataFromUUIDFromDB(selectedUUID);
        canevaSteps->testSteps(acceleroData);
        statusBar->showMessage(tr("Ouverture compteur de pas"));
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
