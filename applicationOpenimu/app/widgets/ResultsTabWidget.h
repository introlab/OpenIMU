#ifndef RESULTSTABWIDGET_H
#define RESULTSTABWIDGET_H

#include <QWidget>
#include <QVBoxLayout>
#include <string>
#include <QLabel>
#include <QtCharts/QChartView>
#include <QtCharts/QPieSeries>
#include <QtCharts/QPieSlice>
#include "../algorithm/AlgorithmOutput.h"
#include "../algorithm/AlgorithmList.h"

class ResultsTabWidget: public QWidget
{
    Q_OBJECT

    public:
    ResultsTabWidget();
    ResultsTabWidget(QWidget *parent, AlgorithmInfo &algoInfo, AlgorithmOutput &output);
     ~ResultsTabWidget();

    public slots:

    private:
    QVBoxLayout* layout;

    QLabel* algoName;
    QWidget* container;
    QLabel* imuType;

};

#endif
