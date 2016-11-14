#ifndef RESULTSTABWIDGET_H
#define RESULTSTABWIDGET_H

#include <QWidget>
#include <QtWidgets>
#include <QVBoxLayout>
#include <string>
#include <QLabel>
#include <QtCharts/QChartView>
#include <QtCharts/QPieSeries>
#include <QtCharts/QPieSlice>
#include "../algorithm/AlgorithmOutput.h"
#include "../algorithm/AlgorithmList.h"
#include <QPushButton>

QT_CHARTS_USE_NAMESPACE

class ResultsTabWidget: public QWidget
{
    Q_OBJECT

    public:
    ResultsTabWidget();
    ResultsTabWidget(QWidget *parent, RecordInfo &recordInfo, AlgorithmInfo &algoInfo, AlgorithmOutput &output);
     ~ResultsTabWidget();

    public slots:
    void exportToPdfSlot();

    private:
    QVBoxLayout* layout;
    QWidget* container;
    QLabel* imuType;
    QPushButton* exportToPdf;
    RecordInfo m_recordInfo;
    QChartView *chartView;

    QLabel* algoLabel;
    QLabel* recordLabel;
    QLabel* dateLabel;
    QLabel* startHourLabel;
    QLabel* endHourLabel;
    QLabel* positionLabel;
    QLabel* measureUnitLabel;
    QLabel* computeTimeLabel;

    void init(AlgorithmInfo &algoInfo, AlgorithmOutput &output);
};

#endif
