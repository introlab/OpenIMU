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

private:
    QChart * chart;
    QChartView *chartView;
    QLineSeries *lineseriesX;
    QLineSeries *lineseriesY;
    QLineSeries *lineseriesZ;
    QSlider *slider;
    QWidget *centralWidget;
    QVBoxLayout* layout;
    AccelerometerReader* accReader;
    vector<SensorDataPerDay> availableData;
};

#endif // ACCDATADISPLAY_H
