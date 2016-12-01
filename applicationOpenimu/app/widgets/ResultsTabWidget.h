#ifndef RESULTSTABWIDGET_H
#define RESULTSTABWIDGET_H

#include <QWidget>
#include <QtWidgets>
#include <string>
#include <QLabel>
#include <QtCharts/QChartView>
#include <QtCharts/QPieSeries>
#include <QtCharts/QPieSlice>
#include <QPushButton>
#include <QInputDialog>

#include "../utilities/OpenImuButton.h"
#include "../algorithm/AlgorithmOutputInfoSerializer.h"
#include "../algorithm/AlgorithmInfoSerializer.h"
#include "../acquisition/RecordInfo.h"
#include "../core/components/blockType/DbBlock.h"
#include "../MainWindow.h"
#include "../AccDataDisplay.h"

QT_CHARTS_USE_NAMESPACE

class ResultsTabWidget: public QWidget
{
    Q_OBJECT

public:
    ResultsTabWidget();
    ResultsTabWidget(QWidget *parent, AlgorithmOutputInfo output);
    ResultsTabWidget(QWidget *parent, AccDataDisplay* AccDataDisplay);
     ~ResultsTabWidget();

    void init(AlgorithmOutputInfo output);
    void initFilterView(AccDataDisplay* accDataDisplay);

public slots:
    void exportToPdfSlot();
    void exportToDBSlot();

private:
    QWidget* m_parent;
    QGridLayout* layout;
    QWidget* container;
    QLabel* imuType;
    OpenImuButton* exportToPdf;
    OpenImuButton* saveResultsToDB;
    QChartView *chartView;

    QLabel* algoLabel;
    QLabel* recordLabel;
    QLabel* dateLabel;
    QLabel* positionLabel;
    QLabel* computeTimeLabel;

    DbBlock * m_databaseAccess;

    AlgorithmOutputInfo m_algorithmOutputInfo;
};

#endif
