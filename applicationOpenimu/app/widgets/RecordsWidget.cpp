#include "RecordsWidget.h"

RecordsWidget::RecordsWidget(QWidget *parent,WimuAcquisition data, RecordInfo rcd):QWidget(parent)
{
    layout = new QGridLayout;
    this->setLayout(layout);

    acceleroData = data;
    record = rcd;

    recordTitle = new QLabel("Nom de l'enregistrement: "+ QString::fromStdString(record.m_recordName));
    recordDate = new QLabel(QString::fromStdString("Journée d'enregistrement: ")+ QString::fromStdString(acceleroData.getDates().back().date));
    imuType = new QLabel("Centralle inertielle: "+ QString::fromStdString(record.m_imuType));
    positionImu = new QLabel("Position IMU: "+ QString::fromStdString(record.m_imuPosition));
    detailsRecord = new QLabel("Détails enregistrement: "+ QString::fromStdString(record.m_recordDetails));
    seeFullGraphBtn = new QPushButton("Graphique détaillé");
    goToNextStep = new QPushButton("Choisir Algorithme");

    AccDataDisplay *dataDisplay = new AccDataDisplay(acceleroData);
    dataDisplay->showSimplfiedDataDisplay();

    layout->addWidget(recordTitle,0,0);
    layout->addWidget(recordDate,1,0);
    layout->addWidget(imuType,2,0);
    layout->addWidget(positionImu,3,0);
    layout->addWidget(detailsRecord,4,0);
    layout->addWidget(dataDisplay,5,0,1,2);
    layout->addWidget(seeFullGraphBtn,6,0);
    layout->addWidget(goToNextStep,6,3);

    this->setStyleSheet( "QPushButton{"
                         "background-color: rgba(230, 233, 239,1);"
                         "border-style: inset;"
                         "border-width: 2px;"
                         "border-radius: 10px;"
                         "border-color: white;"
                         "font: 12px;"
                         "min-width: 10em;"
                         "padding: 6px; }"
     );

    connect(seeFullGraphBtn, SIGNAL(clicked()), this, SLOT(openFullGraphSlot()));
    connect(goToNextStep, SIGNAL(clicked()), parent, SLOT(openAlgorithmTab()));
    fDialog = new FullGraphDialog(acceleroData);
}

RecordsWidget::~RecordsWidget()
{

}
void RecordsWidget::openFullGraphSlot(){

    if(!fDialog->isVisible())
    {
        fDialog->show();
    }
}
