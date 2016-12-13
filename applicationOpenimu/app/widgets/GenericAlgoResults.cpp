#include "GenericAlgoResults.h"
#include "ui_genericalgoresults.h"
#include<QDebug>
#include<QtCharts/QChartView>
#include<QtCharts/QPieSeries>
#include<QtCharts/QPieSlice>
#include <QTextEdit>
#include <QJsonDocument>

GenericAlgoResults::GenericAlgoResults(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::GenericAlgoResults)
{
    ui->setupUi(this);
}

GenericAlgoResults::~GenericAlgoResults()
{
    delete ui;
}

GenericAlgoResults::GenericAlgoResults(QWidget *parent, AlgorithmOutputInfo algoOutput, std::string json):
    QWidget(parent),
    ui(new Ui::GenericAlgoResults)
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

     // Display formatted Json

         QJsonDocument doc = QJsonDocument::fromJson(json.c_str());
         QString formattedJsonString = doc.toJson(QJsonDocument::Indented);
         QTextEdit* rawResponse = new QTextEdit(formattedJsonString);

        ui->graphLayout->addWidget(rawResponse);

}
