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
#include "acquisition/AccelerometerReader.h"

QT_CHARTS_USE_NAMESPACE

class AccDataDisplay : public QObject
{
    Q_OBJECT

public:
    AccDataDisplay();
    AccDataDisplay(std::string filePath);
    QWidget *getCentralView();
    void fillChartSeries(int i);
public slots:
    void sliderValueChanged(int value);
    void slotDisplayXAxis(int value);
    void slotDisplayYAxis(int value);
    void slotDisplayZAxis(int value);

private:
    QChart * chart;
    QChartView *chartView;
    QLineSeries *lineseriesX;
    QLineSeries *lineseriesY;
    QLineSeries *lineseriesZ;

    QCheckBox *checkboxX;
    QCheckBox *checkboxY;
    QCheckBox *checkboxZ;

    QSlider *slider;
    QWidget *centralWidget;
    QVBoxLayout* layout;
    AccelerometerReader* accReader;
    vector<SensorDataPerDay> availableData;
};

#endif // ACCDATADISPLAY_H
