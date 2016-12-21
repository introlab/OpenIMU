#include "RecordsDialog.h"
#include <QFileDialog>
#include <QString>
#include<QFile>
#include<QMessageBox>
#include<QtDebug>
#include <fstream>
#include <string>
#include <iostream>

#include "../MainWindow.h"
#include"acquisition/WimuAcquisition.h"
#include "acquisition/CJsonSerializer.h"



RecordsDialog::RecordsDialog(QWidget *parent):QDialog(parent)
{

    m_parent = parent;
    m_current_uuid = "";

    this->setMinimumSize(300,400);
    this->setMaximumSize(300,400);
    this->setWindowTitle(QWidget::tr("Enregistrements"));

    m_mainLayout = new QGridLayout(this);
    m_selectRecord = new QPushButton("");
    QIcon img(":/icons/parcourir.png");
    m_selectRecord->setIcon(img);
    m_selectRecord->setIconSize(QSize(105,35));
    m_selectRecord->setFlat(true);
    m_selectRecord->setCursor(Qt::PointingHandCursor);
    m_selectRecord->setMaximumWidth(105);
    m_selectRecord->setStyleSheet("border:none");
    m_folderSelected = new QLabel(QWidget::tr("Dossier séléctionné:"));

    m_selectedImuLabel = new QLabel(QWidget::tr("Centrale inertielle:"));
    m_imuSelectComboBox = new QComboBox;
    m_imuSelectComboBox->setMinimumHeight(20);
    m_imuSelectComboBox->addItem(QWidget::tr("WimU"));
    m_imuSelectComboBox->addItem(QWidget::tr("Deslys trigno"));
    m_imuSelectComboBox->addItem(QWidget::tr("XSens"));
    m_selectedImu = new QLabel(QWidget::tr("None"));

    m_imuPosition = new QLabel(tr("Position: "));
    m_imuPositionComboBox = new QComboBox;
    m_imuPositionComboBox ->setMinimumHeight(20);
    m_imuPositionComboBox->addItem(QWidget::tr("Poignet"));
    m_imuPositionComboBox->addItem(QWidget::tr("Hanche"));
    m_imuPositionComboBox->addItem(QWidget::tr("Cheville"));
    m_imuPositionComboBox->addItem(QWidget::tr("Genoux"));
    m_imuPositionComboBox->addItem(QWidget::tr("Coude"));
    m_imuPositionComboBox->addItem(QWidget::tr("Tête"));
    m_imuPositionComboBox->addItem(QWidget::tr("Cou"));

    m_recordNaming = new QLabel(tr("Nom de l'enregistrement*:"));
    m_recordName = new QLineEdit;
    m_recordName->setMinimumHeight(20);
    m_recordName->setPlaceholderText(QWidget::tr("Wimu_2016_10_18_PatientX"));

    m_recordDetails = new QLabel(tr("Détails de l'enregistrement: "));
    m_userDetails = new QTextEdit();
    m_userDetails->setMinimumHeight(20);
    m_userDetails->setMaximumHeight(100);
    m_addRecord = new QPushButton("");
    m_addRecord->setCursor(Qt::PointingHandCursor);
    QIcon imgadd(":/icons/charger.png");
    m_addRecord->setIcon(imgadd);
    m_addRecord->setIconSize(QSize(105,35));
    m_addRecord->setFlat(true);
    m_addRecord->setMaximumWidth(105);
    m_addRecord->setStyleSheet("border:none");
    m_spinner = new QLabel();
    m_movie = new QMovie("../applicationOpenimu/app/icons/upload_loader.gif");
    m_spinner->setMovie(m_movie);

    m_successLabel = new QLabel();

    m_mainLayout->addWidget(m_selectRecord,0,0,Qt::AlignCenter);

    m_mainLayout->addWidget(m_folderSelected,1,0);

    m_mainLayout->addWidget(m_selectedImuLabel,2,0);
    m_mainLayout->addWidget(m_imuSelectComboBox,3,0);
    m_mainLayout->addWidget(m_imuPosition,4,0);
    m_mainLayout->addWidget(m_imuPositionComboBox,5,0);

    m_mainLayout->addWidget(m_recordNaming,6,0);
    m_mainLayout->addWidget(m_recordName,7,0);

    m_mainLayout->addWidget(m_recordDetails,8,0);
    m_mainLayout->addWidget(m_userDetails,9,0);

    m_mainLayout->addWidget(m_addRecord,10,0,Qt::AlignCenter);

    m_mainLayout->addWidget(m_spinner,11,0,Qt::AlignCenter);

    m_mainLayout->addWidget(m_successLabel,11,0,Qt::AlignCenter);

    connect(m_addRecord, SIGNAL(clicked()), this, SLOT(addRecordSlot()));

    connect(m_selectRecord, SIGNAL(clicked()), this, SLOT(selectRecordSlot()));
    connect(m_imuSelectComboBox, SIGNAL(currentIndexChanged(QString)), m_selectedImu, SLOT(setText(QString)));

}

RecordsDialog::~RecordsDialog()
{

}


void RecordsDialog::selectRecordSlot()
{
    QFile *file;
    m_folderToAdd = QFileDialog::getExistingDirectory(this, tr("Sélectionner dossier"),"/path/to/file/");
    file = new QFile(m_folderToAdd);
    if(!m_folderToAdd.isEmpty()){
        m_folderSelected->setText(tr("Dossier séléctionné: ")+ file->fileName().section("/",-1,-1));
        m_isFolderSelected = true;
    }else{
        m_folderSelected->setText(tr(" Aucun dossier séléctionné ") + file->fileName());
        m_isFolderSelected = false;
    }
}

//*************************** ADD RECORD SLOT *************************
bool RecordsDialog::addRecordFileListToBD(QStringList & fileList, std::string folderPath)
{
    std::string output;
    bool validFolder = false;

    for (int i=0; i<fileList.count(); i++)
    {
        std::string filePathAcc = "";
        std::string filePathGyr = "";
        std::string filePathMag = "";
        validFolder = false;

        if(fileList[i].contains("ACC"))
        {
            filePathAcc =  folderPath +"/"+fileList[i].toStdString();
            validFolder = true;

        }
        else if(fileList[i].contains("GYR"))
        {
            filePathGyr =  folderPath +"/"+fileList[i].toStdString();
            validFolder = true;
        }
        else if(fileList[i].contains("MAG"))
        {
            filePathMag =  folderPath +"/"+fileList[i].toStdString();
            validFolder = true;
        }

        if(validFolder && !m_recordName->text().isEmpty() && m_isFolderSelected  )
        {
            WimuAcquisition* wimuData = new WimuAcquisition(filePathAcc,filePathGyr,filePathMag,50);
            wimuData->initialize();
            RecordInfo recordInfo;
            recordInfo.m_recordName = m_recordName->text().toStdString();
            recordInfo.m_imuType = m_imuSelectComboBox->currentText().toStdString();
            recordInfo.m_imuPosition = m_imuPositionComboBox->currentText().toStdString();
            recordInfo.m_recordDetails = m_userDetails->toPlainText().toStdString();
            recordInfo.m_parentId = "None";
            CJsonSerializer::Serialize(wimuData,recordInfo, output);
            QString outputString = QString::fromStdString(output);

            if(m_current_uuid.isEmpty())
            {
                addRecordInDB(outputString,true);
            }
            else
            {
                addRecordInDB(outputString,false);
            }
        }
        else if(m_recordName->text().isEmpty() && !m_isFolderSelected)
        {
            return false;
        }
    }
    return true;
}
void RecordsDialog::addRecordSlot()
{
    MainWindow * mainWindow = (MainWindow*)m_parent;
    mainWindow->setStatusBarText(tr("Insertion de l'enregistrement dans la base de données en cours..."));
    mainWindow->startSpinner();

    m_successLabel->setText("");

    QDir* dir = new QDir(m_folderToAdd);
    dir->setFilter(QDir::Files | QDir::NoDotAndDotDot | QDir::NoSymLinks);

    QFileInfoList list = dir->entryInfoList(QDir::Files | QDir::NoDotAndDotDot | QDir::Dirs);
    bool addingRecordSuccess = true;

    foreach(QFileInfo finfo, list)
    {
        if (finfo.isDir()) {

            QString messageStatus = "Extraction des données de " + finfo.absoluteFilePath();
            mainWindow->setStatusBarText(messageStatus);
            QDir* subDir = new QDir(finfo.absoluteFilePath());
            QStringList fileList = subDir->entryList();
            if(!addRecordFileListToBD(fileList,finfo.absoluteFilePath().toStdString()))
            {
                QMessageBox messageBox;
                messageBox.warning(0,tr("Avertissement"), "Vérifier le nom de l'enregistrement et qu'un dossier a été séléctionné");
                messageBox.setFixedSize(500,200);
                addingRecordSuccess = false;
                break;
            }
        }
        else
        {
            QStringList fileList = dir->entryList();
            QString messageStatus = "Extraction des données de " + finfo.absoluteFilePath();
            mainWindow->setStatusBarText(messageStatus);
            if(!addRecordFileListToBD(fileList,m_folderToAdd.toStdString()))
            {
                QMessageBox messageBox;
                messageBox.warning(0,tr("Avertissement"), "Vérifier le nom de l'enregistrement et qu'un dossier a été séléctionné");
                messageBox.setFixedSize(500,200);
                addingRecordSuccess = false;
                break;
            }
            break;
        }
    }


    if(addingRecordSuccess && !m_isDuplicateName)
    {

        m_successLabel->setText(tr("L'enregistrement ")+m_recordName->text()+tr(" à été ajouté avec succès"));
        mainWindow->setStatusBarText(tr("L'enregistrement ")+m_recordName->text()+tr(" à été ajouté avec succès"), MessageStatus::success);

        m_current_uuid = "";
        QMainWindow* currWin = (QMainWindow*)m_parent;
        MainWindow* win = (MainWindow*)currWin;
        win->getRecordsFromDB();
        this->close();
    }
    else if (m_isDuplicateName)
    {
        m_successLabel->setText(m_error_msg);
        mainWindow->setStatusBarText(m_error_msg, MessageStatus::error);

        QMainWindow* currWin = (QMainWindow*)m_parent;
        MainWindow* win = (MainWindow*)currWin;
        win->getRecordsFromDB();
    }

    mainWindow->stopSpinner(true);
}

//*************************** DATA BASE ACCESS *************************

// Insert single records

bool RecordsDialog::addRecordInDB(QString& json, bool isSingleRecord)
{
    QNetworkAccessManager *manager = new QNetworkAccessManager();
    QByteArray dataByteArray (json.toStdString().c_str(),json.toStdString().length());                                                                                                                  //Your webservice URL
    QNetworkRequest request;
    if(isSingleRecord)
    {
        request.setUrl(QUrl("http://127.0.0.1:5000/insertrecord"));
    }
    else
    {
        request.setUrl(QUrl("http://127.0.0.1:5000/insertrecord/concat/"+ m_current_uuid));
    }

    QByteArray postDataSize = QByteArray::number(dataByteArray.size());
    request.setRawHeader("User-Agent", "ApplicationNameV01");
    request.setRawHeader("Content-Type", "application/json");
    request.setRawHeader("Content-Length", postDataSize);

    if (manager) {
        bool result;

        QNetworkReply *reply = manager->post(request, dataByteArray);

        QEventLoop loop;
        result = connect(manager, SIGNAL(finished(QNetworkReply*)), &loop,SLOT(quit()));
        loop.exec();
        reponseRecue(reply);

    }
    return true;
}

void RecordsDialog::reponseRecue(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
    {
        std::string strJson = reply->readAll();
        Json::Value root;
        Json::Reader reader;
        bool parsingSuccessful = reader.parse( strJson.c_str(), root );     //parse process
        if ( !parsingSuccessful )
        {
            std::cout  << "Failed to parse"
                       << reader.getFormattedErrorMessages();
        }
        m_current_uuid = QString::fromStdString(root.get("valeuruuid", "A Default Value if not exists" ).asString());
        m_isDuplicateName = false;
    }
    else
    {
        std::string strJson = reply->readAll();
        Json::Value root;
        Json::Reader reader;
        bool parsingSuccessful = reader.parse( strJson.c_str(), root );     //parse process
        if ( !parsingSuccessful )
        {
            std::cout  << "Failed to parse"
                       << reader.getFormattedErrorMessages();
        }
        m_error_msg = QString::fromStdString(root.get("message", "A Default Value if not exists" ).asString()).compare("DuplicateKeyError") == 0 ? "Erreur: Le nom d'enregistrement existe déjà" : "Connection error";
        if(m_error_msg.compare("Connection error") !=0)
        {
            m_isDuplicateName = true;
        }
    }
    delete reply;
}
