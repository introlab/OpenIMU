#include "StepCounterResults.h"
#include "ui_StepCounterResults.h"
#include<QDebug>

StepCounterResults::StepCounterResults(QWidget *parent) :
    QWidget(parent),
    m_ui(new Ui::StepCounterResults)
{
    m_ui->setupUi(this);
}

StepCounterResults::~StepCounterResults()
{
    delete m_ui;
}

StepCounterResults::StepCounterResults(QWidget *parent, AlgorithmOutputInfo algoOutput):
    QWidget(parent),
    m_ui(new Ui::StepCounterResults)
{
    m_ui->setupUi(this);
    // Données
    m_ui->imuType->setText(QString::fromStdString(algoOutput.m_recordType));
    m_ui->recordName->setText(QString::fromStdString(algoOutput.m_recordName));
    m_ui->imuPosition->setText(QString::fromStdString(algoOutput.m_recordImuPosition));

    // Algorithme
    m_ui->algorithmName->setText(QString::fromStdString(algoOutput.m_algorithmName));
    m_ui->dateApplication->setText(QString::fromStdString(algoOutput.m_date));
    m_ui->computeTime->setText(QString::fromStdString(std::to_string(algoOutput.m_executionTime)) + "ms");
    m_ui->results->setText(QString::fromStdString(std::to_string(algoOutput.m_value)));

    //** Paramètres

    for(int i=0; i<algoOutput.m_algorithmParameters.size();i++)
    {
        if(algoOutput.m_algorithmParameters.at(i).m_name.compare("uuid") !=0)
        {
            QLabel* qLabel = new QLabel;
            qLabel->setText(QString::fromStdString(algoOutput.m_algorithmParameters.at(i).m_name)+":" +QString::fromStdString(algoOutput.m_algorithmParameters.at(i).m_value));
            m_ui->parameterLayout->addWidget(qLabel);
        }
    }

    //SLOTS
    connect(m_ui->exportToPdf, SIGNAL(clicked()), parent, SLOT(exportToPdfSlot()));
    connect(m_ui->saveToBd, SIGNAL(clicked()), parent, SLOT(exportToDBSlot()));

}
void StepCounterResults::hideButtons()
{
    m_ui->exportToPdf->hide();
    m_ui->saveToBd->hide();
}
