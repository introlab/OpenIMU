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
#include "acquisition/WimuAcquisition.h"
#include "widgets/RangeSlider.h"
#include "graph/DataChart.h"
#include "graph/ChartView.h"

QT_CHARTS_USE_NAMESPACE

class AccDataDisplay : public QWidget
{
    Q_OBJECT

public:
    AccDataDisplay();
    AccDataDisplay(std::string filePath);
    void fillChartSeries();

public slots:

    void slotDisplayXAxis(int value);
    void slotDisplayYAxis(int value);
    void slotDisplayZAxis(int value);
    void slotDisplayNorme(int value);
    void slotDisplayMovingAverage(int value);
    std::vector<signed short> movingAverage(int windowSize);
    void leftSliderValueChanged(int value);
    void rightSliderValueChanged(int value);

private:
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

    RangeSlider *rSlider;
    QVBoxLayout* layout;

    WimuAcquisition * acceleroData;
    std::vector<frame> availableData;
    std::vector<frame> sliceData;
};

#endif // ACCDATADISPLAY_H
