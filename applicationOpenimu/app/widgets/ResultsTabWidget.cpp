#include "ResultsTabWidget.h"

QT_CHARTS_USE_NAMESPACE

ResultsTabWidget::ResultsTabWidget(QWidget *parent,AlgorithmInfo &algoInfo, AlgorithmOutput &output):QWidget(parent)
{
    layout = new QVBoxLayout;
    this->setLayout(layout);

    algoName = new QLabel(QString::fromStdString(algoInfo.name));
    recordDate = new QLabel("Journée d'enregistrement: ");


    layout->addWidget(algoName);
    layout->addWidget(recordDate);

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
}

ResultsTabWidget::ResultsTabWidget()
{

}

ResultsTabWidget::~ResultsTabWidget()
{

}
