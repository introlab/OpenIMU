#ifndef RESULTSTABWIDGET_H
#define RESULTSTABWIDGET_H

#include <QWidget>
#include <QtWidgets>
#include <string>
#include <QLabel>
#include <QtCharts/QChartView>
#include <QtCharts/QPieSeries>
#include <QtCharts/QPieSlice>
#include "../algorithm/AlgorithmOutputInfoSerializer.h"
#include "../algorithm/AlgorithmInfoSerializer.h"
#include "../acquisition/RecordInfo.h"
#include "../core/components/blockType/DbBlock.h"
#include <QPushButton>

QT_CHARTS_USE_NAMESPACE

class ResultsTabWidget: public QWidget
{
    Q_OBJECT

    public:
    ResultsTabWidget();
    ResultsTabWidget(QWidget *parent, RecordInfo &recordInfo, AlgorithmInfo algoInfo, AlgorithmOutputInfo output);
     ~ResultsTabWidget();

    public slots:
    void exportToPdfSlot();
    void exportToDBSlot();

    private:
    QGridLayout* layout;
    QWidget* container;
    QLabel* imuType;
    QPushButton* exportToPdf;
    QPushButton* saveResultsToDB;
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

    DbBlock * m_databaseAccess;

    AlgorithmOutputInfo m_algorithmOutputInfo;

    void init(AlgorithmInfo algoInfo, AlgorithmOutputInfo output);
};

#endif
