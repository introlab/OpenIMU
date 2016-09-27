#include "RecordsDialog.h"
#include <QFileDialog>
#include <QString>
#include<QFile>

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
    QString folderToAdd = QFileDialog::getExistingDirectory(this, tr("Sélectionner dossier"),"/path/to/file/");
    file = new QFile(folderToAdd);
    if(!folderToAdd.isEmpty()){
         folderSelected->setText(tr("Dossier séléctionné: ")+ file->fileName().section("/",-1,-1));
     }else{
          folderSelected->setText(tr(" Aucun dossier séléctionné ") + file->fileName());
     }
}

void RecordsDialog::addRecordSlot()
{
    databaseAccess = new DbBlock;
    databaseAccess->addRecordInDB(recordName->text(),selectedImu->text(),folderSelected->text());
    databaseAccess->requete(recordName->text(),selectedImu->text());

    successLabel->setText(recordName->text()+tr(" ajouté avec succès"));
    mainLayout->addWidget(successLabel);
    mainLayout->setAlignment(successLabel,Qt::AlignCenter);
}
