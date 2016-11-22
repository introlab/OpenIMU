#include "RecordsWidget.h"
#include <QInputDialog>
#include<QDir>
#include"../MainWindow.h"

RecordsWidget::RecordsWidget(QWidget *parent,const WimuAcquisition& data, RecordInfo rcd):QWidget(parent)
{
    renameRecordClicked = false;
    this->setStyleSheet( "QPushButton{"
                         "background-color: rgba(119, 160, 175, 0.7);"
                         "border-style: inset;"
                         "border-width: 2px;"
                         "border-radius: 10px;"
                         "border-color: white;"
                         "font: 12px;"
                         "min-width: 10em;"
                         "padding: 6px; }"
                         "QPushButton:pressed { background-color: rgba(70, 95, 104, 0.7);}"
     );

    QVBoxLayout * mainLayout = new QVBoxLayout();
    layout = new QGridLayout;
    mainLayout->addSpacing(20);
    mainLayout->addLayout(layout);
    mainLayout->addSpacing(20);
    this->setLayout(mainLayout);

    acceleroData = data;
    record = rcd;

    recordTitle = new QLabel(QString::fromStdString(record.m_recordName));
    recordTitle->setFont(QFont( "Arial", 12, QFont::Bold));

    if(acceleroData.getDates().size()>0)
    {
        recordDate = new QLabel(QString::fromStdString("Journée d'enregistrement: ")+ QString::fromStdString(acceleroData.getDates().back().date));
    }
    else
    {
        recordDate = new QLabel("Enregistrement invalide");
    }

    imuType = new QLabel("Centralle inertielle: "+ QString::fromStdString(record.m_imuType));
    positionImu = new QLabel("Position IMU: "+ QString::fromStdString(record.m_imuPosition));
    detailsRecord = new QLabel("Détails enregistrement: "+ QString::fromStdString(record.m_recordDetails));
    seeFullGraphBtn = new QPushButton("Graphique détaillé");
    goToNextStep = new QPushButton("Choisir Algorithme");
    deleteBtn = new QPushButton("Supprimer enregistrement");
    AccDataDisplay *dataDisplay = new AccDataDisplay(acceleroData);
    dataDisplay->showSimplfiedDataDisplay();

    editRecord = new QPushButton("Renommer");
    editRecord->setMaximumWidth(20);
    editRecord->setIcon(QIcon(":/../icons/edit.png"));
    editRecord->setStyleSheet("background-image:url(:C:/Users/stef/Documents/OpenIMU/applicationOpenimu/app/icons/edit.png);");
    QHBoxLayout * recordTitleLayout = new QHBoxLayout();
    recordNameEdit = new QLineEdit();
    recordNameEdit->setText(recordTitle->text());
    recordNameEdit->setStyleSheet("QLineEdit { qproperty-frame: false }");
    recordNameEdit->setReadOnly(true);
    recordTitleLayout->addWidget( new QLabel("Nom de l'enregistrement: "));
    recordTitleLayout->addWidget(recordNameEdit);
    recordTitleLayout->addWidget(editRecord);
    //layout->addWidget(recordTitle,0,0);
    layout->addLayout(recordTitleLayout,0,0);
    layout->addWidget(deleteBtn,0,3);
    layout->addWidget(recordDate,1,0);
    layout->addWidget(imuType,2,0);
    layout->addWidget(positionImu,3,0);
    layout->addWidget(detailsRecord,4,0);
    layout->addWidget(dataDisplay,5,0,1,2);
    layout->addWidget(seeFullGraphBtn,6,0);
    layout->addWidget(goToNextStep,6,3);
    layout->setHorizontalSpacing(100);

    deleteBtn->setStyleSheet("background-color: rgba(209, 31, 58, 0.6);");
    connect(seeFullGraphBtn, SIGNAL(clicked()), this, SLOT(openFullGraphSlot()));
    connect(seeFullGraphBtn, SIGNAL(clicked()), this, SLOT(openFullGraphSlot()));
    connect(goToNextStep, SIGNAL(clicked()), parent, SLOT(openAlgorithmTab()));
    connect(deleteBtn, SIGNAL(clicked()), parent, SLOT(deleteRecord()));
    connect(editRecord, SIGNAL(clicked()), this, SLOT(renameRecord()));
    fDialog = new FullGraphDialog();
    fDialog->prepareDisplay(acceleroData,record);
}

RecordsWidget::~RecordsWidget()
{

}
void RecordsWidget::openFullGraphSlot()
{
    if(!fDialog->isVisible())
    {
        fDialog->show();
    }
}

void RecordsWidget::renameRecord()
{
    if(!renameRecordClicked)
    {
        recordNameEdit->setReadOnly(false);
        recordNameEdit->setStyleSheet("QLineEdit {qproperty-frame: true }");
        renameRecordClicked = true;
        editRecord->setText("Valider");

    }
    else
    {
        MainWindow * mainWindow = (MainWindow*)m_parent;
        mainWindow->renameRecordFromUUID(record.m_recordId,recordNameEdit->text().toStdString());
        qDebug() << "here";
        recordNameEdit->setReadOnly(true);
        recordNameEdit->setStyleSheet("QLineEdit {qproperty-frame: false }");
        renameRecordClicked = false;
    }

}
