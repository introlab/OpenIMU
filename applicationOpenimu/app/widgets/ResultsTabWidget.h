#ifndef RESULTSTABWIDGET_H
#define RESULTSTABWIDGET_H

#include <QWidget>
#include <QVBoxLayout>
#include <string>
#include <QLabel>
#include <QtCharts/QChartView>
#include <QtCharts/QPieSeries>
#include <QtCharts/QPieSlice>
#include "CustomQmlScene.h"
#include "../core/Caneva.h"
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
    QLabel* recordDate;
    QWidget* container;
    QLabel* imuType;

};

#endif
