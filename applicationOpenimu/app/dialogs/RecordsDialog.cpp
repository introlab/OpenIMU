#include "RecordsDialog.h"
#include <QFileDialog>
#include <QString>
#include<QFile>
#include<QMessageBox>
#include "../MainWindow.h"
#include"acquisition/WimuAcquisition.h"
#include "acquisition/CJsonSerializer.h"
#include<QtDebug>
#include <fstream>
#include <string>
#include <iostream>


RecordsDialog::RecordsDialog(QWidget *parent):QDialog(parent)
{

    m_parent = parent;

    this->setMinimumSize(300,400);
    this->setMaximumSize(300,400);
    this->setWindowTitle(QWidget::tr("Enregistrements"));

    mainLayout = new QGridLayout(this);
    selectRecord = new QPushButton(QWidget::tr("Sélectionner un enregistrement"));
    folderSelected = new QLabel(QWidget::tr("Dossier séléctionné:"));

    selectedImuLabel = new QLabel(QWidget::tr("Centrale inertielle:"));
    imuSelectComboBox = new QComboBox;
    imuSelectComboBox->addItem(QWidget::tr("WimU"));
    imuSelectComboBox->addItem(QWidget::tr("Deslys trigno"));
    imuSelectComboBox->addItem(QWidget::tr("XSens"));
    selectedImu = new QLabel(QWidget::tr("None"));

    imuPosition = new QLabel(tr("Position: "));
    imuPositionComboBox = new QComboBox;
    imuPositionComboBox->addItem(QWidget::tr("Poignet"));
    imuPositionComboBox->addItem(QWidget::tr("Hanche"));
    imuPositionComboBox->addItem(QWidget::tr("Cheville"));
    imuPositionComboBox->addItem(QWidget::tr("Genoux"));
    imuPositionComboBox->addItem(QWidget::tr("Coude"));
    imuPositionComboBox->addItem(QWidget::tr("Tête"));
    imuPositionComboBox->addItem(QWidget::tr("Cou"));

    recordNaming = new QLabel(tr("Nom de l'enregistrement*:"));
    recordName = new QLineEdit;
    recordName->setMinimumHeight(20);
    recordName->setPlaceholderText(QWidget::tr("Wimu_2016_10_18_PatientX"));

    recordDetails = new QLabel(tr("Détails de l'enregistrement: "));
    userDetails = new QTextEdit();
    userDetails->setMinimumHeight(20);
    userDetails->setMaximumHeight(100);
    addRecord = new QPushButton(QWidget::tr("Ajouter l'enregistrement"));

    spinner = new QLabel();
    movie = new QMovie("../applicationOpenimu/app/icons/upload_loader.gif");
    spinner->setMovie(movie);

    successLabel = new QLabel();

    mainLayout->addWidget(selectRecord,0,0);

    mainLayout->addWidget(folderSelected,1,0);

    mainLayout->addWidget(selectedImuLabel,2,0);
    mainLayout->addWidget(imuSelectComboBox,3,0);
    mainLayout->addWidget(imuPosition,4,0);
    mainLayout->addWidget(imuPositionComboBox,5,0);

    mainLayout->addWidget(recordNaming,6,0);
    mainLayout->addWidget(recordName,7,0);

    mainLayout->addWidget(recordDetails,8,0);
    mainLayout->addWidget(userDetails,9,0);

    mainLayout->addWidget(addRecord,10,0);

    mainLayout->addWidget(spinner,11,0,Qt::AlignCenter);

    mainLayout->addWidget(successLabel,11,0,Qt::AlignCenter);

    connect(addRecord, SIGNAL(clicked()), this, SLOT(addRecordSlot()));

    connect(selectRecord, SIGNAL(clicked()), this, SLOT(selectRecordSlot()));
    connect(imuSelectComboBox, SIGNAL(currentIndexChanged(QString)), selectedImu, SLOT(setText(QString)));

    this->setStyleSheet( "QPushButton{"
                         "background-color: rgba(119, 160, 175,0.7);"
                         "border-style: inset;"
                         "border-width: 0.2px;"
                         "border-radius: 10px;"
                         "border-color: white;"
                         "font: 12px;"
                         "min-width: 10em;"
                         "padding: 6px; }"
                         "QPushButton:pressed { background-color: rgba(70, 95, 104, 0.7);}"
                         );
}

RecordsDialog::~RecordsDialog()
{

}


void RecordsDialog::selectRecordSlot()
{
    QFile *file;
    folderToAdd = QFileDialog::getExistingDirectory(this, tr("Sélectionner dossier"),"/path/to/file/");
    file = new QFile(folderToAdd);
    if(!folderToAdd.isEmpty()){
         folderSelected->setText(tr("Dossier séléctionné: ")+ file->fileName().section("/",-1,-1));
         isFolderSelected = true;
     }else{
          folderSelected->setText(tr(" Aucun dossier séléctionné ") + file->fileName());
          isFolderSelected = false;
     }
}

void RecordsDialog::addRecordSlot()
{
    spinner->show();
    movie->start();
    QString msgErreur="";
    MainWindow * mainWindow = (MainWindow*)m_parent;
    mainWindow->setStatusBarText(tr("Insertion de l'enregistrement dans la base de données en cours..."));

    successLabel->setText("");

    QDir* dir = new QDir(folderToAdd);
    dir->setFilter(QDir::Files | QDir::NoDotAndDotDot | QDir::NoSymLinks);
    //qDebug() << "Scanning: " << dir->path();
    QStringList fileList = dir->entryList();
    std::string output;
    std::string filePathAcc = "";
    std::string filePathGyr = "";
    std::string filePathMag = "";
    bool validFolder = false;
    for (int i=0; i<fileList.count(); i++)
    {
        if(fileList[i].contains("ACC"))
        {
        filePathAcc = folderToAdd.toStdString()+"/"+fileList[i].toStdString();
        validFolder = true;
        }
        else if(fileList[i].contains("GYR"))
        {
        filePathGyr = folderToAdd.toStdString()+"/"+fileList[i].toStdString();
        validFolder = true;
        }
        else if(fileList[i].contains("MAG"))
        {
        filePathMag = folderToAdd.toStdString()+"/"+fileList[i].toStdString();
        validFolder = true;
        }
    }

    if(recordName->text().isEmpty() || !isFolderSelected || !validFolder)
    {
        if(recordName->text().isEmpty() && !isFolderSelected)
            msgErreur = tr("Veuillez sélectionner un dossier et ajoutez un nom d'enregistrement");

        else if(!isFolderSelected)
        {
            msgErreur = tr("Veuillez sélectionner un dossier");
        }
        else if(recordName->text().isEmpty())
            msgErreur = tr("Ajoutez un nom d'enregistrement");
        else if(!validFolder)
            msgErreur = tr("Le dossier choisi est invalide");


        QMessageBox messageBox;

        messageBox.warning(0,tr("Avertissement"),msgErreur);
        messageBox.setFixedSize(500,200);
        }
    else
    {

        WimuAcquisition* acceleroData = new WimuAcquisition(filePathAcc,filePathGyr,filePathMag,50);
        acceleroData->initialize();

        RecordInfo info;
        info.m_recordName = recordName->text().toStdString();
        info.m_imuType = imuSelectComboBox->currentText().toStdString();
        info.m_imuPosition = imuPositionComboBox->currentText().toStdString();
        info.m_recordDetails = userDetails->toPlainText().toStdString();
        CJsonSerializer::Serialize(acceleroData,info,"", output);
        databaseAccess = new DbBlock;
        QString temp = QString::fromStdString(output);//TODO remove
        databaseAccess->addRecordInDB(temp);
        successLabel->setText(tr("L'enregistrement ")+recordName->text()+tr(" à été ajouté avec succès"));
        mainWindow->setStatusBarText(tr("L'enregistrement ")+recordName->text()+tr(" à été ajouté avec succès"));
    }
    movie->stop();
    spinner->hide();
}

void RecordsDialog::reject()
{
    QMainWindow* currWin = (QMainWindow*)m_parent;
    MainWindow* win = (MainWindow*)currWin;
    win->getRecordsFromDB();
    QDialog::reject();
}
