#include "RecordsDialog.h"
#include <QFileDialog>
#include <QString>

RecordsDialog::RecordsDialog(QWidget *parent):QDialog(parent)
{
    this->setMinimumSize(300,200);
    this->setWindowTitle(QString::fromUtf8("Enregistrements"));


    mainLayout = new QVBoxLayout(this);
    selectRecord = new QPushButton("Sélectionner un enregistrement");
    addRecord = new QPushButton("Ajouter enregistrement");
    fileSelected = new QLabel("Fichier sélectionné");
    recordName = new QLineEdit;
    imuSelect = new QComboBox;

    recordName->setMinimumHeight(20);
    recordName->setPlaceholderText(tr("Nom de l'enregistrement"));
    imuSelect->addItem(tr("WimU"));
    imuSelect->addItem(tr("Deslys trigno"));
    imuSelect->addItem(tr("XSens"));

    mainLayout->addSpacing(10);
    mainLayout->addWidget(selectRecord);
    mainLayout->addSpacing(5);
    mainLayout->addWidget(imuSelect);
    mainLayout->addWidget(recordName);
    mainLayout->addWidget(fileSelected);
    mainLayout->addSpacing(5);
    mainLayout->addWidget(addRecord);
    mainLayout->addSpacing(10);

    connect(addRecord, SIGNAL(clicked()), this, SLOT(addRecordSlot()));
    connect(selectRecord, SIGNAL(clicked()), this, SLOT(selectRecordSlot()));

    this->setStyleSheet(         "QPushButton{"
                                 "background-color: rgba(239, 73, 73,0.7);"
                                 "border-style: inset;"
                                 "border-width: 2px;"
                                 "border-radius: 10px;"
                                 "border-color: white;"
                                 "font: 12px;"
                                 "min-width: 10em;"
                                 "padding: 6px; }"
                                 );
}

RecordsDialog::~RecordsDialog()
{

}


void RecordsDialog::selectRecordSlot()
{
    QString folderToAdd = QFileDialog::getExistingDirectory(this, tr("Sélectionner dossier"),"/path/to/file/");
     if(!folderToAdd.isEmpty()){
         fileSelected->setText(QString::fromStdString("Dossier séléctionné: ")+ folderToAdd);
     }else{
          fileSelected->setText(QString::fromStdString(" Aucun dossier séléctionné ")+ folderToAdd);
     }
}

void RecordsDialog::addRecordSlot()
{
    this->accept();
}
