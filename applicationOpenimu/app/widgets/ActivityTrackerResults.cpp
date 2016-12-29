#include "ActivityTrackerResults.h"
#include "ui_activitytrackerresults.h"
#include<QDebug>
#include<QtCharts/QChartView>
#include<QtCharts/QPieSeries>
#include<QtCharts/QPieSlice>

ActivityTrackerResults::ActivityTrackerResults(QWidget *parent) :
    QWidget(parent),
    m_ui(new Ui::ActivityTrackerResults)
{
    m_ui->setupUi(this);
}

ActivityTrackerResults::~ActivityTrackerResults()
{
    delete m_ui;
}

ActivityTrackerResults::ActivityTrackerResults(QWidget *parent, AlgorithmOutputInfo algoOutput):
    QWidget(parent),
    m_ui(new Ui::ActivityTrackerResults)
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

    // GRAPH
    QtCharts::QChartView* chartView = new QtCharts::QChartView();
    QtCharts::QPieSeries *series = new QtCharts::QPieSeries();
    series->setHoleSize(0.35);
    QtCharts::QPieSlice *slice = series->append("Temps actif: " + QString::fromStdString(std::to_string(algoOutput.m_value)) + " %" , algoOutput.m_value);
    slice->setExploded();
    slice->setLabelVisible();
    series->append("Temps passif: " +  QString::fromStdString(std::to_string(100-algoOutput.m_value)) + " %", algoOutput.m_value-100);
    chartView->setRenderHint(QPainter::Antialiasing);
    chartView->chart()->setTitle("Temps d'activité");
    chartView->chart()->setTitleFont(QFont("Arial", 14));
    chartView->chart()->addSeries(series);
    chartView->chart()->legend()->setAlignment(Qt::AlignBottom);
    chartView->chart()->setTheme(QtCharts::QChart::ChartThemeLight);
    chartView->chart()->setAnimationOptions(QtCharts::QChart::SeriesAnimations);
    chartView->chart()->legend()->setFont(QFont("Arial", 12));
    chartView->setMinimumHeight(500);
    chartView->setMinimumWidth(300);
    m_ui->graphLayout->addWidget(chartView);

    //SLOTS
    connect(m_ui->exportToPdf, SIGNAL(clicked()), parent, SLOT(exportToPdfSlot()));
    connect(m_ui->saveToBd, SIGNAL(clicked()), parent, SLOT(exportToDBSlot()));
}

void ActivityTrackerResults::hideButtons(){
    m_ui->exportToPdf->hide();
    m_ui->saveToBd->hide();
}
