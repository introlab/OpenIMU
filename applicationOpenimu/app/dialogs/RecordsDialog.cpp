#include "RecordsDialog.h"
#include <QFileDialog>
#include <QString>
#include<QFile>
#include"acquisition/WimuAcquisition.h"
#include "acquisition/CJsonSerializer.h"
#include<QtDebug>
#include <fstream>
#include <string>
#include <iostream>

RecordsDialog::RecordsDialog(QWidget *parent):QDialog(parent)
{
    this->setMinimumSize(300,310);

    this->setWindowTitle(QWidget::tr("Enregistrements"));

    mainLayout = new QGridLayout(this);
    selectRecord = new QPushButton(QWidget::tr("Sélectionner un enregistrement"));
    addRecord = new QPushButton(QWidget::tr("Ajouter l'enregistrement"));
    folderSelected = new QLabel(QWidget::tr("Fichier sélectionné"));
    recordName = new QLineEdit;
    imuSelectComboBox = new QComboBox;
    selectedImu = new QLabel(QWidget::tr("None"));
    successLabel = new QLabel();
    recordNaming = new QLabel(tr("Nom de l'enregistrement:"));
    recordName->setMinimumHeight(20);
    recordName->setPlaceholderText(QWidget::tr("Wimu_2016_10_18_PatientX"));

    imuSelectComboBox->addItem(QWidget::tr("WimU"));
    imuSelectComboBox->addItem(QWidget::tr("Deslys trigno"));
    imuSelectComboBox->addItem(QWidget::tr("XSens"));

    imuPosition = new QLabel(tr("Position: "));
    imuPositionComboBox = new QComboBox;
    imuPositionComboBox->addItem(QWidget::tr("Poignet"));
    imuPositionComboBox->addItem(QWidget::tr("Hanche"));
    imuPositionComboBox->addItem(QWidget::tr("Cheville"));
    imuPositionComboBox->addItem(QWidget::tr("Genoux"));
    imuPositionComboBox->addItem(QWidget::tr("Coude"));
    imuPositionComboBox->addItem(QWidget::tr("Tête"));
    imuPositionComboBox->addItem(QWidget::tr("Cou"));

    recordDetails = new QLabel(tr("Détails de l'enregistrement: "));
    userDetails = new QLineEdit();
    userDetails->setMinimumHeight(20);

    spinner = new QLabel();
    movie = new QMovie("../applicationOpenimu/app/icons/upload_loader.gif");

    spinner->setMovie(movie);
    mainLayout->addWidget(selectRecord,0,0);

    mainLayout->addWidget(imuSelectComboBox,1,0);

    mainLayout->addWidget(imuPosition,2,0);
    mainLayout->addWidget(imuPositionComboBox,3,0);

    mainLayout->addWidget(recordDetails,4,0);
    mainLayout->addWidget(userDetails,5,0);

    mainLayout->addWidget(recordNaming,6,0);
    mainLayout->addWidget(recordName,7,0);

    mainLayout->addWidget(folderSelected,8,0);

    mainLayout->addWidget(addRecord,9,0);

    mainLayout->addWidget(spinner,10,0,Qt::AlignCenter);

    mainLayout->addWidget(successLabel,11,0,Qt::AlignCenter);

    connect(addRecord, SIGNAL(clicked()), this, SLOT(addRecordSlot()));
    connect(selectRecord, SIGNAL(clicked()), this, SLOT(selectRecordSlot()));
    connect(imuSelectComboBox, SIGNAL(currentIndexChanged(QString)), selectedImu, SLOT(setText(QString)));

    this->setStyleSheet(         "QPushButton{"
                                 "background-color: rgba(239, 73, 73,0.7);"
                                 "border-style: inset;"
                                 "border-width: 2px;"
                                 "border-radius: 10px;"
                                 "border-color: white;"
                                 "font: 12px;"
                                 "min-width: 10em;"
                                 "padding: 6px; }"
                                 "QPushButton:pressed {"
                                 "background-color: rgba(82, 165, 92, 0.7);"
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
     }else{
          folderSelected->setText(tr(" Aucun dossier séléctionné ") + file->fileName());
     }
}

void RecordsDialog::addRecordSlot()
{
    spinner->show();
    movie->start();

    QDir* dir = new QDir(folderToAdd);
      dir->setFilter(QDir::Files | QDir::NoDotAndDotDot | QDir::NoSymLinks);
      qDebug() << "Scanning: " << dir->path();
      QStringList fileList = dir->entryList();
      std::string output;
      std::string filePathAcc = "";
      std::string filePathGyr = "";
      std::string filePathMag = "";

      for (int i=0; i<fileList.count(); i++)
      {
          if(fileList[i].contains("ACC"))
          {
              qDebug() << "Found file: " << fileList[i];
              filePathAcc = folderToAdd.toStdString()+"/"+fileList[i].toStdString();
              qDebug() << QString::fromStdString(filePathAcc);
          }
          else if(fileList[i].contains("GYR"))
          {
              qDebug() << "Found file: " << fileList[i];
              filePathGyr = folderToAdd.toStdString()+"/"+fileList[i].toStdString();
              qDebug() << QString::fromStdString(filePathGyr);
          }
          else if(fileList[i].contains("MAG"))
          {
              qDebug() << "Found file: " << fileList[i];
              filePathMag = folderToAdd.toStdString()+"/"+fileList[i].toStdString();
              qDebug() << QString::fromStdString(filePathMag);
          }
      }

      WimuAcquisition* acceleroData = new WimuAcquisition(filePathAcc,filePathGyr,filePathMag,50);
      acceleroData->initialize();

      RecordInfo info;
      info.m_recordName = recordName->text().toStdString();
      info.m_imuType = imuSelectComboBox->currentText().toStdString();
      info.m_imuPosition = imuPositionComboBox->currentText().toStdString();
      info.m_recordDetails = userDetails->text().toStdString();
      CJsonSerializer::Serialize(acceleroData,info,"", output);
      qDebug("OUTPUT:");
      QString qstr = QString::fromStdString(output);
      qDebug()<<qstr;
      std::ofstream out("recordToAdd.json");
      out << output;
      out.close();


    databaseAccess = new DbBlock;
    databaseAccess->addRecordInDB(QString::fromStdString(output));

    movie->stop();
    spinner->hide();

    successLabel->setText(recordName->text()+tr(" Ajouté avec succès"));
}
