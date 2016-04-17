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
#include "newAcquisition/wimuacquisition.h"
#include "rangeslider.h"

QT_CHARTS_USE_NAMESPACE

class AccDataDisplay : public QWidget
{
    Q_OBJECT

public:
    AccDataDisplay();
    AccDataDisplay(std::string filePath);
    void fillChartSeries();

public slots:
    void sliderValueChanged(int value);
    void slotDisplayXAxis(int value);
    void slotDisplayYAxis(int value);
    void slotDisplayZAxis(int value);
    void leftSliderValueChanged(int value);
    void rightSliderValueChanged(int value);

private:
    QChart * chart;
    QChartView *chartView;
    QLineSeries *lineseriesX;
    QLineSeries *lineseriesY;
    QLineSeries *lineseriesZ;

    QCheckBox *checkboxX;
    QCheckBox *checkboxY;
    QCheckBox *checkboxZ;

    RangeSlider *rSlider;
    QSlider *slider;
    QVBoxLayout* layout;

    WimuAcquisition * acceleroData;
    std::vector<frame> availableData;
    std::vector<frame> sliceData;
};

#endif // ACCDATADISPLAY_H
