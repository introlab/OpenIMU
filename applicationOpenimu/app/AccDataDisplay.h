#ifndef ACCDATADISPLAY_H
#define ACCDATADISPLAY_H

#include <iostream>
#include <QtCharts/QChartView>
#include <QVBoxLayout>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QLegend>
#include <QtCharts/QValueAxis>
#include <QSlider>
#include <QCheckBox>
#include <QTextEdit>
#include <QLineEdit>
#include <QPushButton>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QNetworkAccessManager>
#include <QGroupBox>

#include "acquisition/WimuAcquisition.h"
#include "widgets/RangeSlider.h"
#include "graph/DataChart.h"
#include "graph/ChartView.h"
#include"../../acquisition/CJsonSerializer.h"
#include"../../acquisition/WimuRecord.h"
#include "core/components/blockType/DbBlock.h"

QT_CHARTS_USE_NAMESPACE

class AccDataDisplay : public QWidget
{
    Q_OBJECT

public:
    AccDataDisplay();
    AccDataDisplay( const WimuAcquisition& accData);
    void fillChartSeries();
    void leftSliderValueChanged(double value);
    void rightSliderValueChanged(double value);
    void showSimplfiedDataDisplay();
    void setInfo(RecordInfo recInfo);

public slots:

    void slotDisplayXAxis(int value);
    void slotDisplayYAxis(int value);
    void slotDisplayZAxis(int value);
    void slotDisplayNorme(int value);
    void slotDisplayMovingAverage(int value);
    std::vector<signed short> movingAverage(int windowSize);
    void handleResetZoomBtn();
    void firstUpdated(const QVariant &v);
    void secondUpdated(const QVariant &v);
    void slotSaveNewSetRange();

private:
    QGroupBox *groupBoxAxes;
    QGroupBox *groupBoxSlider;
    QGroupBox *groupBoxSave;

    DataChart * chart;
    ChartView *chartView;
    QLineSeries *lineseriesX;
    QLineSeries *lineseriesY;
    QLineSeries *lineseriesZ;
    QLineSeries *lineseriesAccNorm;
    QLineSeries *lineseriesMovingAverage;

    QCheckBox *checkboxX;
    QCheckBox *checkboxY;
    QCheckBox *checkboxZ;
    QCheckBox *checkboxAccNorm;
    QCheckBox *checkboxMovingAverage;
    QLabel* dateRecorded;
    QPushButton*pbtn;
    QLabel* recordNaming;
    QLineEdit *recordName;
    QLabel* recordDetails;
    QTextEdit* userDetails;
    QPushButton* saveDataSet;
    RangeSlider *rSlider;
    QVBoxLayout* layout;

    std::vector<frame> availableData;
    std::vector<frame> sliceData;
    DbBlock * databaseAccess;
    RecordInfo m_recordInfo;

    double rSliderValue;
    double lSliderValue;
};

#endif // ACCDATADISPLAY_H
