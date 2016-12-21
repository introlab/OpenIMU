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
    m_ui(new Ui::GenericAlgoResults)
{
    m_ui->setupUi(this);
}

GenericAlgoResults::~GenericAlgoResults()
{
    delete m_ui;
}

GenericAlgoResults::GenericAlgoResults(QWidget *parent, AlgorithmOutputInfo algoOutput, std::string json):
    QWidget(parent),
    m_ui(new Ui::GenericAlgoResults)
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

    // Display formatted Json

    QJsonDocument doc = QJsonDocument::fromJson(json.c_str());
    QString formattedJsonString = doc.toJson(QJsonDocument::Indented);
    QTextEdit* rawResponse = new QTextEdit(formattedJsonString);

    m_ui->graphLayout->addWidget(rawResponse);

}
