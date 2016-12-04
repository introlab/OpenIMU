#include "StepCounterResults.h"
#include "ui_StepCounterResults.h"
#include<QDebug>

StepCounterResults::StepCounterResults(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::StepCounterResults)
{
    ui->setupUi(this);
}

StepCounterResults::~StepCounterResults()
{
    delete ui;
}

StepCounterResults::StepCounterResults(QWidget *parent, AlgorithmOutputInfo algoOutput):
    QWidget(parent),
    ui(new Ui::StepCounterResults)
{
      ui->setupUi(this);
    // Données
     ui->imuType->setText(QString::fromStdString(algoOutput.m_recordType));
     ui->recordName->setText(QString::fromStdString(algoOutput.m_recordName));
     ui->imuPosition->setText(QString::fromStdString(algoOutput.m_recordImuPosition));

    // Algorithme
     ui->algorithmName->setText(QString::fromStdString(algoOutput.m_algorithmName));
     ui->dateApplication->setText(QString::fromStdString(algoOutput.m_date));
     ui->computeTime->setText(QString::fromStdString(std::to_string(algoOutput.m_executionTime)) + "ms");
     ui->results->setText(QString::fromStdString(std::to_string(algoOutput.m_value)));

     //** Paramètres

     for(int i=0; i<algoOutput.m_algorithmParameters.size();i++)
     {
         if(algoOutput.m_algorithmParameters.at(i).m_name.compare("uuid") !=0)
         {

             QLabel* temp = new QLabel;
             temp->setText(QString::fromStdString(algoOutput.m_algorithmParameters.at(i).m_name)+":" +QString::fromStdString(algoOutput.m_algorithmParameters.at(i).m_value));
             ui->parameterLayout->addWidget(temp);

         }
     }

     //SLOTS
     connect(ui->exportToPdf, SIGNAL(clicked()), parent, SLOT(exportToPdfSlot()));
     connect(ui->saveToBd, SIGNAL(clicked()), parent, SLOT(exportToDBSlot()));

}
