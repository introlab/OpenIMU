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
#include <QByteArray>
#include "widgets/RecordViewWidget.h"
#include <QFileDialog>

QT_CHARTS_USE_NAMESPACE

MainWindow *g_mainWindow = NULL;

void myMessageOutput(QtMsgType type, const QMessageLogContext &context, const QString &msg)
  {
      QString result;
      QByteArray localMsg = msg.toLocal8Bit();
      switch (type) {
      case QtDebugMsg:
          result = QString("Debug: %1 (1%2:%3, %4)\n")
                  .arg(QString(localMsg))
                  .arg(QString(context.file))
                  .arg(QString::number(context.line))
                  .arg(QString(context.function));
          fprintf(stderr, "Debug: %s (%s:%u, %s)\n", localMsg.constData(), context.file, context.line, context.function);
          break;
      case QtInfoMsg:
          result = QString("Info: %1 (1%2:%3, %4)\n")
                  .arg(QString(localMsg))
                  .arg(QString(context.file))
                  .arg(QString::number(context.line))
                  .arg(QString(context.function));
          fprintf(stderr, "Info: %s (%s:%u, %s)\n", localMsg.constData(), context.file, context.line, context.function);
          break;
      case QtWarningMsg:
          result = QString("Warning: %1 (1%2:%3, %4)\n")
                  .arg(QString(localMsg))
                  .arg(QString(context.file))
                  .arg(QString::number(context.line))
                  .arg(QString(context.function));

          fprintf(stderr, "Warning: %s (%s:%u, %s)\n", localMsg.constData(), context.file, context.line, context.function);
          break;
      case QtCriticalMsg:
          result = QString("Critical: %1 (1%2:%3, %4)\n")
                  .arg(QString(localMsg))
                  .arg(QString(context.file))
                  .arg(QString::number(context.line))
                  .arg(QString(context.function));

          fprintf(stderr, "Critical: %s (%s:%u, %s)\n", localMsg.constData(), context.file, context.line, context.function);
          break;
      case QtFatalMsg:
          result = QString("Fatal: %1 (1%2:%3, %4)\n")
                  .arg(QString(localMsg))
                  .arg(QString(context.file))
                  .arg(QString::number(context.line))
                  .arg(QString(context.function));

          fprintf(stderr, "Fatal: %s (%s:%u, %s)\n", localMsg.constData(), context.file, context.line, context.function);
          abort();
      }

      g_mainWindow->displayDebugMessage(result);
  }


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), m_apiProcess(NULL)
{

    //Create debug widget
    m_debugTextEdit = new QTextEdit(this);
    m_debugTextEdit->setReadOnly(true);

    //Add Redirection
    //TODO not clean, but working
    g_mainWindow = this;

    qInstallMessageHandler(myMessageOutput);
    //create dbAccess
    databaseAccess = new DbBlock;



    this->setWindowIcon(QIcon("../applicationOpenimu/app/icons/logo.ico"));
    this->setStyleSheet("background-color:white;");

    this->setWindowTitle(QString::fromUtf8("OpenIMU"));
    this->setMinimumSize(1024,768);

    QFont font;
    font.setFamily("Open Sans Regular");
    font.setKerning(false);
    font.setPointSize(12);

    QFont fontitem;
    fontitem.setFamily("Open Sans Regular");
    fontitem.setKerning(false);
    fontitem.setPointSize(11);

    QFont fontTabWidget;
    fontTabWidget.setFamily("Open Sans Light");
    fontTabWidget.setKerning(false);
    fontTabWidget.setPointSize(12);

    menu = new ApplicationMenuBar(this);
    statusBar = new QStatusBar(this);
    statusBar->setFont(fontitem);
    mainWidget = new MainWidget(this);
    listWidget = new myTreeWidget(this);

    listWidget->setHeaderHidden(true);

    tabWidget = new QTabWidget;

    spinnerStatusBar = new QLabel;
    movieSpinnerBar = new QMovie("../applicationOpenimu/app/icons/loaderStatusBar.gif");

    spinnerStatusBar->setMovie(movieSpinnerBar);

    this->setMenuBar(menu);
    this->setStatusBar(statusBar);

    statusBar->setStyleSheet("background-color:rgba(230, 233, 239,0.2);");
    statusBar->setMinimumHeight(100);
    listWidget->setFont(fontitem);
    listWidget->setCursor(Qt::PointingHandCursor);
    listWidget->setStyleSheet("border:none;"
                              "background-color:white;"
                              "opacity:0;");

    QLabel* explorateurLabel = new QLabel("Explorateur");
    explorateurLabel->setFont(font);
    explorateurLabel->setStyleSheet("color:grey;"
                                    "background-color:rgba(255,255,255,0);");

    QPushButton* addRecord = new QPushButton("");
    addRecord->setCursor(Qt::PointingHandCursor);
    addRecord->setFlat(true);
    addRecord->setFont(font);
    addRecord->setStyleSheet("color:#3498db;");
    QIcon img(":/icons/nouveau.png");
    addRecord->setIcon(img);
    addRecord->setIconSize(QSize(100,45));

    QPushButton* deleteRecord = new QPushButton("");
    QIcon imgDelete(":/icons/supprimer.png");
    deleteRecord->setIcon(imgDelete);
    deleteRecord->setIconSize(QSize(100,40));
    deleteRecord->setFlat(true);
    deleteRecord->setFont(font);
    deleteRecord->setStyleSheet("color:#e74c3c;");
    deleteRecord->setCursor(Qt::PointingHandCursor);

    QFrame* topLine = new QFrame();
    topLine->setFrameShape(QFrame::HLine);
    topLine->setStyleSheet("color:#7f8c8d;");

    QFrame* backLine = new QFrame();
    backLine->setFrameShape(QFrame::HLine);
    backLine->setStyleSheet("color:#7f8c8d;");

    QFrame* backLineDelete = new QFrame();
    backLineDelete->setFrameShape(QFrame::HLine);
    backLineDelete->setStyleSheet("color:#7f8c8d;");

    QVBoxLayout* vlayout = new QVBoxLayout();
    vlayout->addWidget(explorateurLabel);
    vlayout->addWidget(listWidget);
    vlayout->addWidget(topLine);
    vlayout->addWidget(addRecord);
    vlayout->addWidget(backLine);
    vlayout->addWidget(deleteRecord);
    vlayout->addWidget(backLineDelete);
    mainWidget->m_mainLayout->addLayout(vlayout);

    listWidget->setMaximumWidth(150);
    tabWidget->setTabsClosable(true);
    homeWidget = new HomeWidget(this);
    tabWidget->addTab(homeWidget,tr("Accueil"));
    tabWidget->setStyleSheet("background-color: rgba(247, 250, 255,0);");
    tabWidget->setCurrentWidget(tabWidget->widget(0));
    tabWidget->setFont(fontTabWidget);
    tabWidget->grabGesture(Qt::PanGesture);
    tabWidget->grabGesture(Qt::PinchGesture);

    //Add debug tab
    int index = tabWidget->addTab(m_debugTextEdit,tr("Console"));


    mainWidget->m_mainLayout->addWidget(tabWidget);

    setCentralWidget(mainWidget);
    setStatusBarText(tr("Prêt"));
    statusBar->setMinimumHeight(20);
    statusBar->addPermanentWidget(spinnerStatusBar);

    //Execute launchApi in a thread
    //QtConcurrent::run(MainWindow::launchApi,this);
    launchApi();


    connect(tabWidget, SIGNAL(tabCloseRequested(int)), this, SLOT(closeTab(int)));
    connect(tabWidget, SIGNAL(currentChanged(int)), this, SLOT(onTabChanged(int)));
    connect(addRecord, SIGNAL(clicked()), this, SLOT(openRecordDialog()));
    connect(deleteRecord, SIGNAL(clicked()), this, SLOT(deleteRecordFromList()));

    getSavedResultsFromDB();
    getRecordsFromDB();



}

MainWindow::~MainWindow(){

    qDebug("MainWindow::~MainWindow()");

    if (m_apiProcess)
    {
        //Write CTRL-C
        //char ctrlC = 0x03;
        //m_apiProcess->write(&ctrlC);

        m_apiProcess->close();
        qDebug("Waiting for backend to finish");
        m_apiProcess->waitForFinished();
    }

    delete menu ;
}

void MainWindow::onListItemClicked(QTreeWidgetItem* item, int column)
{
    for(int i=0; i<record.m_WimuRecordList.size();i++)
    {
        if(record.m_WimuRecordList.at(i).m_recordName.compare(item->text(column).toStdString()) == 0)
        {
            selectedRecord = record.m_WimuRecordList.at(i);
        }
    }
}

void MainWindow::onListItemDoubleClicked(QTreeWidgetItem* item, int column)
{
    setStatusBarText(tr("Chargement de l'enregistrement..."));
    startSpinner();

    bool isRecord = false;
    for(int i=0; i<record.m_WimuRecordList.size();i++)
    {
        if(record.m_WimuRecordList.at(i).m_recordName.compare(item->text(column).toStdString()) == 0)
        {
            selectedRecord = record.m_WimuRecordList.at(i);

            getDataFromUUIDFromDB(selectedRecord.m_recordId);

            //Check if Data is corrupt
            if(wimuAcquisition.getDataSize()<=0)
            {
                QMessageBox msgBox(
                            QMessageBox::Question,
                            trUtf8("Avertissement"),
                            "L'enregistrement sélectionné est corrompu. Voulez-vous le supprimer?",
                            QMessageBox::Yes | QMessageBox::No);

                msgBox.setButtonText(QMessageBox::Yes, "Oui");
                msgBox.setButtonText(QMessageBox::No, "Non");

                if (msgBox.exec() == QMessageBox::Yes) {
                  deleteRecordFromUUID(selectedRecord.m_recordId);
                  refreshRecordListWidget();
                }
            }
            else
            {
               RecordViewWidget* recordTab = new RecordViewWidget(this,wimuAcquisition,selectedRecord);
               addTab(recordTab,selectedRecord.m_recordName);
            }
            isRecord = true;
        }        
    }
    //If the item clicked is not a Record, it means that it is a Result.
    if(!isRecord)
    {
        setStatusBarText(tr("Chargement du résultat..."));
        for(int i=0; i<savedResults.m_algorithmOutputList.size();i++)
        {
            if(savedResults.m_algorithmOutputList.at(i).m_resultName.compare(item->text(column).toStdString()) == 0)
            {
                ResultsTabWidget* resultTab = new ResultsTabWidget(this,savedResults.m_algorithmOutputList.at(i),true);
                addTab(resultTab,savedResults.m_algorithmOutputList.at(i).m_resultName);
            }
        }
    }
    stopSpinner();
    setStatusBarText(tr("Prêt"));
}

void MainWindow::startSpinner()
{
    spinnerStatusBar->show();
    movieSpinnerBar->start();
}

void MainWindow::stopSpinner(bool playAudio)
{
    movieSpinnerBar->stop();
    spinnerStatusBar->hide();

    if(playAudio)
    {
        Utilities utilities;
        utilities.playAudio();
    }
}

void MainWindow:: refreshRecordListWidget()
{
    bool successGettingResults = getSavedResultsFromDB();
    bool successGettingRecords = getRecordsFromDB();
}

void MainWindow::openRecordDialog()
{
    rDialog = new RecordsDialog(this);
    rDialog->show();
}

void MainWindow::openAlgorithmTab()
{
    algorithmTab = new AlgorithmTab(this,selectedRecord);
    addTab(algorithmTab,"Algorithmes: "+selectedRecord.m_recordName);
}

void MainWindow::setStatusBarText(QString txt, MessageStatus status)
{
    QString styleSheet = "color: " + Utilities::getColourFromEnum(status) +";";
    statusBar->setStyleSheet(styleSheet);

    statusBar->showMessage(tr(txt.toStdString().c_str()));
}

void MainWindow::displayDebugMessage(const QString &message)
{
    m_debugTextEdit->append(message);
}

void MainWindow::deleteRecord()
{
    startSpinner();
    setStatusBarText("Suppression de l'enregistrement...");

    QMessageBox msgBox;
    msgBox.setText("Suppression de l'enregistrement");
    msgBox.setInformativeText("Êtes vous sûr de vouloir supprimer cet enregistrement?");

    msgBox.setStandardButtons(QMessageBox::Ok | QMessageBox::Cancel);
    msgBox.setDefaultButton(QMessageBox::Cancel);
    int ret = msgBox.exec();

    switch (ret) {
      case QMessageBox::Ok:
        deleteRecordFromUUID(selectedRecord.m_recordId);
        getRecordsFromDB();
        wimuAcquisition.clearData();
        selectedRecord.m_recordId = "";
        tabWidget->removeTab(tabWidget->currentIndex());
        openHomeTab();
          break;
      case QMessageBox::Cancel:
        // Cancel was clicked
        setStatusBarText("Suppression de l'enregistrement annulée...");
        break;
      default:
          // should never be reached
        setStatusBarText("Prêt");
          break;
    }

    stopSpinner(true);
}

void MainWindow::openHomeTab()
{
    homeWidget = new HomeWidget(this);
    addTab(homeWidget,"Accueil");
}

void MainWindow::addAlgo()
{
    QString fileName = QFileDialog::getOpenFileName(this,
        "Sélectionner un script", QStandardPaths::displayName(QStandardPaths::DocumentsLocation), "Fichier de script (*.py)");

    QString destFile = "../PythonAPI/lib/algos/" + fileName.split("/").last();

    bool copySucessful = QFile::copy(fileName, destFile);

    if(copySucessful)
    {
        setStatusBarText("L'ajout s'est déroulé avec succès");
    }
    else
    {
        setStatusBarText("Une erreur s'est produite. (Le fichier existe déjà?)");
    }
}

void MainWindow::apiProcessFinished()
{
    qDebug() << "void MainWindow::apiProcessFinished()";
    //m_apiProcess->deleteLater();
    //m_apiProcess = NULL;
}

void MainWindow::readyReadStdOutput()
{
    if (m_apiProcess)
    {
        QByteArray stdOutput = m_apiProcess->readAllStandardOutput();
        m_debugTextEdit->append("---------API PROCESS (Output) ---------");
        m_debugTextEdit->append(QString::fromUtf8(stdOutput));
    }
}

void MainWindow::readyReadStdError()
{
    if (m_apiProcess)
    {
        QByteArray stdError = m_apiProcess->readAllStandardError();
        m_debugTextEdit->append("---------API PROCESS (Error) ---------");
        m_debugTextEdit->append(QString::fromUtf8(stdError));
    }

}

void MainWindow::launchApi(){

    //Be careful we are in separate thread here

    qDebug() << "Launching python API";
    m_apiProcess = new QProcess(this);

    //TODO get the result of the python script (stdout, stderr)
#ifdef __APPLE__
    qDebug() << "ApplicationDirPath:" << QApplication::applicationDirPath();
    m_apiProcess->setWorkingDirectory(QApplication::applicationDirPath() + "/PythonAPI/src");
    m_apiProcess->start("python", QStringList() << "tornado_wsgi.py");
    connect(m_apiProcess,SIGNAL(finished(int)),this,SLOT(apiProcessFinished()));
    connect(m_apiProcess,SIGNAL(readyReadStandardOutput()),this,SLOT(readyReadStdOutput()));
    connect(m_apiProcess,SIGNAL(readyReadStandardError()),this,SLOT(readyReadStdError()));
    m_apiProcess->waitForStarted();

    //Give time for the socket server to start...
    QThread::usleep(100000); //100ms
#else
    parent->m_apiProcess->start("cmd.exe", QStringList() << "/c" << "..\\PythonAPI\\src\\runapi.bat");
    parent->m_apiProcess->waitForFinished(500);
    parent->m_apiProcess->deleteLater();
#endif

    qDebug() << "PythonAPI backend started.";
}



bool MainWindow::getRecordsFromDB()
{
    startSpinner();
    setStatusBarText("Chargement des enregistrements...");

    QNetworkRequest request(QUrl("http://127.0.0.1:5000/records"));
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    manager->get(request);

    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), this ,SLOT(reponseRecue(QNetworkReply*)));

    if(!result)
    {
        setStatusBarText("Erreur de connexion lors de la récupération des enregistrements", MessageStatus::error);
    }

    stopSpinner();
    return result;
}

//Getting results from DB
bool MainWindow::getSavedResultsFromDB()
{
    startSpinner();
    setStatusBarText("Chargement des résultats sauvegardés...");

    QNetworkRequest request(QUrl("http://127.0.0.1:5000/algoResults"));
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QNetworkReply *reply = manager->get(request);

    QEventLoop loop;
    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), &loop,SLOT(quit()));
    loop.exec();
    savedResultsReponse(reply);

    if(!result)
    {
        setStatusBarText("Erreur de connexion lors de la récupération des résultats", MessageStatus::error);
    }

    stopSpinner();
    return result;
}

bool MainWindow::getDataFromUUIDFromDB(std::string uuid)
{
    startSpinner();
    setStatusBarText("Chargement de l'enregistrement...");

    std::string url = "http://127.0.0.1:5000/data?uuid="+uuid;
    QNetworkRequest request(QUrl(QString::fromStdString(url)));
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QNetworkReply *reply = manager->get(request);
    QEventLoop loop;
    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), &loop,SLOT(quit()));

    loop.exec();
    qDebug() << "Reply size: " << reply->header(QNetworkRequest::ContentLengthHeader).toLongLong();
    reponseRecueAcc(reply);

    if(!result)
    {
        setStatusBarText("Erreur de connexion lors de la récupération de l'enregistrement", MessageStatus::error);
    }

    stopSpinner();
    return result;
}

void MainWindow::reponseRecueAcc(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
   {
       wimuAcquisition.clearData();
       std::string testReponse(reply->readAll());

       if(testReponse != "")
       {
           CJsonSerializer::Deserialize(&wimuAcquisition, testReponse);
           setStatusBarText("Enregistrement récupéré");
       }
       else
       {
          setStatusBarText("La requête reçue n'a pas retournée de résultats", MessageStatus::warning);
       }
   }
   else
   {
       setStatusBarText("Erreur de connexion lors de la récupération des enregistrements", MessageStatus::error);
   }
   delete reply;
}

void MainWindow::savedResultsReponse(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
    {
        savedResults.m_algorithmOutputList.clear();
        std::string reponse = reply->readAll().toStdString();

        if(reponse != "")
        {
            savedResults.DeserializeList(reponse);
            setStatusBarText("Enregistrement récupéré");
        }
        else
        {
           setStatusBarText("La requête reçue n'a pas retournée de résultats", MessageStatus::warning);
        }

        setStatusBarText("Prêt");
    }
    else
    {
        setStatusBarText("Erreur lors de la récupération des résultats", MessageStatus::error);
    }
}


void MainWindow::reponseRecue(QNetworkReply* reply)
{
    QFont fontitem;
    fontitem.setFamily("Open Sans Regular");
    fontitem.setKerning(false);
    fontitem.setPointSize(10);

   if (reply->error() == QNetworkReply::NoError)
   {
        std::string testReponse(reply->readAll());

        if(testReponse != "")
        {
            record.m_WimuRecordList.clear();
            CJsonSerializer::Deserialize(&record, testReponse);
            setStatusBarText("Enregistrement récupéré");

            listWidget->clear();
            for(int i=0; i<record.m_WimuRecordList.size();i++)
            {
                QTreeWidgetItem* top_item = new QTreeWidgetItem();
                top_item->setText(0,QString::fromStdString(record.m_WimuRecordList.at(i).m_recordName));
                top_item->setTextColor(0,QColor(117,117,117));

                if(record.m_WimuRecordList.at(i).m_parentId.compare("") == 0 )
                {
                    for(int j=0; j<record.m_WimuRecordList.size();j++)
                    {
                        if(record.m_WimuRecordList.at(j).m_parentId.compare(record.m_WimuRecordList.at(i).m_recordId ) == 0)
                        {
                            QTreeWidgetItem* child_item = new QTreeWidgetItem;
                            child_item->setText(0,QString::fromStdString(record.m_WimuRecordList.at(j).m_recordName));
                            child_item->setIcon(0,*(new QIcon(":/icons/sliced.png")));
                            child_item->setTextColor(0,QColor(117,117,117));
                            top_item->addChild(child_item);
                        }
                    }
                    for(int w = 0; w<savedResults.m_algorithmOutputList.size();w++)
                    {
                        if(savedResults.m_algorithmOutputList.at(w).m_recordId.compare(record.m_WimuRecordList.at(i).m_recordId) == 0)
                        {
                            QTreeWidgetItem* child_item = new QTreeWidgetItem;
                            child_item->setText(0,QString::fromStdString(savedResults.m_algorithmOutputList.at(w).m_resultName));
                            child_item->setIcon(0,*(new QIcon(":/icons/results.png")));
                            child_item->setTextColor(0,QColor(117,117,117));
                            top_item->addChild(child_item);
                        }
                    }
                    listWidget->addTopLevelItem(top_item);
                }
            }

            setStatusBarText("Prêt");
        }
        else
        {
            setStatusBarText("La requête reçue n'a pas retournée de résultats", MessageStatus::warning);
        }
   }
   else
   {
       setStatusBarText("Erreur de connexion lors de la récupération des enregistrements", MessageStatus::error);
   }
   delete reply;
}

//Delete specific record
bool MainWindow::deleteRecordFromUUID(std::string uuid)
{
    startSpinner();
    setStatusBarText("Suppression de l'enregistrement numéro...");

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

    if(!result)
    {
        setStatusBarText("Erreur de connexion lors de la suppression de l'enregistrement", MessageStatus::error);
    }

    stopSpinner();
    return result;
}

//Rename specific record
bool MainWindow::renameRecordFromUUID(std::string uuid, std::string newname)
{
    startSpinner();
    setStatusBarText("Modification du nom de l'enregistrement...");

    std::string url = "http://127.0.0.1:5000/renamerecord/"+uuid+"?name="+newname;

    QNetworkRequest request(QUrl(QString::fromStdString(url)));
    QByteArray dataByteArray (newname.c_str(),newname.length());
    QByteArray postDataSize = QByteArray::number(dataByteArray.size());

    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");
    request.setRawHeader("Content-Length", postDataSize);

    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QNetworkReply *reply = manager->post(request, dataByteArray);

    QEventLoop loop;
    bool result = connect(manager, SIGNAL(finished(QNetworkReply*)), &loop,SLOT(quit()));

    if(!result)
    {
       setStatusBarText("Erreur de connexion lors de la modification du nom de l'enregistrement", MessageStatus::error);
    }

    loop.exec();
    reponseRecueRename(reply);

    stopSpinner();
    return result;
}

bool MainWindow::deleteRecordFromList()
{
    startSpinner();

    if(selectedRecord.m_recordId == "")
    {
        QMessageBox noRecordSelectedMessageBox;
        noRecordSelectedMessageBox.setText("Suppression de l'enregistrement");
        noRecordSelectedMessageBox.setInformativeText("Vous devez sélectionner un enregistrement afin de pouvoir le supprimer.");

        noRecordSelectedMessageBox.setStandardButtons(QMessageBox::Ok | QMessageBox::Cancel);
        noRecordSelectedMessageBox.setDefaultButton(QMessageBox::Cancel);
        noRecordSelectedMessageBox.setWindowIcon(QIcon(":/icons/logo.ico"));
        noRecordSelectedMessageBox.exec();

        return true;
    }

    QMessageBox msgBox;
    msgBox.setText("Suppression de l'enregistrement");
    msgBox.setInformativeText("Êtes vous sûr de vouloir supprimer cet enregistrement?");
    msgBox.setWindowIcon(QIcon(":/icons/logo.ico"));

    msgBox.setStandardButtons(QMessageBox::Ok | QMessageBox::Cancel);
    msgBox.setDefaultButton(QMessageBox::Cancel);
    int ret = msgBox.exec();

    switch (ret) {
      case QMessageBox::Ok:
        deleteRecordFromUUID(selectedRecord.m_recordId);
        getRecordsFromDB();
        break;
    case QMessageBox::Cancel:
        // Cancel was clicked
        break;
    default:
        // should never be reached
        break;
  }
    stopSpinner();
    return true; //TODO: Make void
}
void MainWindow::reponseRecueDelete(QNetworkReply* reply)
{
   if (reply->error() == QNetworkReply::NoError)
   {
       setStatusBarText(tr("Enregistrement effacé avec succès"), MessageStatus::success);
   }
   else
   {
        setStatusBarText(tr("Échec de la suppression de l'enregistrement"), MessageStatus::error);
   }
}

void MainWindow::reponseRecueRename(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
    {
        setStatusBarText(tr("Enregistrement renommé avec succès"), MessageStatus::success);
    }
    else
    {
         setStatusBarText(tr("Échec du changement de nom de l'enregistrement"), MessageStatus::error);
    }
}

void MainWindow::openAbout(){

    aboutDialog = new AboutDialog(this);
    aboutDialog->exec();
}

void MainWindow::openHelp(){
    helpDialog = new HelpDialog(this);
    helpDialog->exec();
}

void MainWindow::addTab(QWidget * tab, std::string label)
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
            tabWidget->setCurrentWidget(tabWidget->widget(i));
        }
    }
    if(found)
    {
        tabWidget->setCurrentWidget(tabWidget->widget(index));
    }
    else
    {
        tabWidget->addTab(tab,QString::fromStdString(label));
        tabWidget->setCurrentWidget(tabWidget->widget(tabWidget->count()-1));
    }

    setStatusBarText(tr("Prêt"));
}
void MainWindow::onTabChanged(int index)
{
    if (index == -1) {
        return;
    }

    for(int i=0; i<record.m_WimuRecordList.size();i++)
    {
        if(record.m_WimuRecordList.at(i).m_recordName.compare(tabWidget->tabText(index).toStdString()) == 0)
        {
            selectedRecord = record.m_WimuRecordList.at(i);
        }
    }
}

void MainWindow::closeTab(int index){

    if (index == -1) {
        return;
    }
    QWidget* tabItem = tabWidget->widget(index);
    if (tabItem != m_debugTextEdit)
    {
        // Removes the tab at position index from this stack of widgets.
        // The page widget itself is not deleted.
        tabWidget->removeTab(index);

        delete(tabItem);
        tabItem = nullptr;
    }
}

void MainWindow::closeWindow(){
    this->close();
}
