#include "ResultsTabWidget.h"
//#include <qlcdnumber.h>

QT_CHARTS_USE_NAMESPACE

ResultsTabWidget::ResultsTabWidget(QWidget *parent,RecordInfo& recordInfo, AlgorithmInfo &algoInfo, AlgorithmOutput &output):QWidget(parent)
{
    m_recordInfo=recordInfo;
    init(algoInfo, output);
}

ResultsTabWidget::ResultsTabWidget(QWidget *parent,AlgorithmInfo &algoInfo, AlgorithmOutput &output):QWidget(parent)
{
    init(algoInfo, output);
}

void ResultsTabWidget::init(AlgorithmInfo &algoInfo, AlgorithmOutput &output)
{
    layout = new QVBoxLayout;
    this->setLayout(layout);

    QString titleName = QString::fromStdString(algoInfo.name);
    titleName += ": ";
    titleName += QString::fromStdString(m_recordInfo.m_recordName);
    algoName = new QLabel(titleName);
    algoName->setFont(QFont( "Arial", 12, QFont::Bold));

    layout->addWidget(algoName);

    if(algoInfo.name == "activityTracker")
    {

        QPieSeries *series = new QPieSeries();
        series->setHoleSize(0.35);
        QPieSlice *slice = series->append("Temps actif:" + QString::fromStdString(std::to_string(output.m_algorithmOutput.value)) + " %" , output.m_algorithmOutput.value);
        slice->setExploded();
        slice->setLabelVisible();
        series->append("Temps passif" +  QString::fromStdString(std::to_string(100-output.m_algorithmOutput.value)) + " %", output.m_algorithmOutput.value-100);


        QChartView *chartView = new QChartView();
        chartView->setRenderHint(QPainter::Antialiasing);
        chartView->chart()->setTitle("Temps d'activité");
        chartView->chart()->setTitleFont(QFont("Arial", 14));
        chartView->chart()->addSeries(series);
        chartView->chart()->legend()->setAlignment(Qt::AlignBottom);
        chartView->chart()->setTheme(QChart::ChartThemeLight);
        chartView->chart()->setAnimationOptions(QChart::SeriesAnimations);
        chartView->chart()->legend()->setFont(QFont("Arial", 12));

        layout->addWidget(chartView);
    }
    else
    {
        QLabel* labelResult = new QLabel(QString::fromStdString(std::to_string(output.m_algorithmOutput.value)) +" pas" );
        algoName->setFont(QFont( "Arial", 12, QFont::Light));
      //  QLCDNumber* number = new QLCDNumber();
      //  number->setDecMode();
      //  number->display(output.m_algorithmOutput.value);
        layout->addWidget(labelResult,Qt::AlignCenter);
        layout->addStretch();
    }
}

ResultsTabWidget::ResultsTabWidget()
{

}

ResultsTabWidget::~ResultsTabWidget()
{

}
