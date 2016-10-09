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
    this->setMinimumSize(300,210);

    this->setWindowTitle(QWidget::tr("Enregistrements"));

    mainLayout = new QVBoxLayout(this);
    selectRecord = new QPushButton(QWidget::tr("Sélectionner un enregistrement"));
    addRecord = new QPushButton(QWidget::tr("Ajouter l'enregistrement"));
    folderSelected = new QLabel(QWidget::tr("Fichier sélectionné"));
    recordName = new QLineEdit;
    imuSelectComboBox = new QComboBox;
    selectedImu = new QLabel(QWidget::tr("None"));
    successLabel = new QLabel();
    recordName->setMinimumHeight(20);
    recordName->setPlaceholderText(QWidget::tr("Nom de l'enregistrement"));
    imuSelectComboBox->addItem(QWidget::tr("WimU"));
    imuSelectComboBox->addItem(QWidget::tr("Deslys trigno"));
    imuSelectComboBox->addItem(QWidget::tr("XSens"));

    mainLayout->addSpacing(10);
    mainLayout->addWidget(selectRecord);
    mainLayout->addSpacing(5);
    mainLayout->addWidget(imuSelectComboBox);
    mainLayout->addWidget(recordName);
    mainLayout->addWidget(folderSelected);
    mainLayout->addSpacing(5);
    mainLayout->addWidget(addRecord);
    mainLayout->addSpacing(10);
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

      CJsonSerializer::Serialize(acceleroData,recordName->text().toStdString(),"", output);
      qDebug("OUTPUT:");
      QString qstr = QString::fromStdString(output);
      qDebug()<<qstr;
      std::ofstream out("recordToAdd.json");
      out << output;
      out.close();


    databaseAccess = new DbBlock;
    databaseAccess->addRecordInDB(QString::fromStdString(output));
    successLabel->setText(recordName->text()+tr(" Ajouté avec succès"));
    mainLayout->addWidget(successLabel);
    mainLayout->setAlignment(successLabel,Qt::AlignCenter);
}
