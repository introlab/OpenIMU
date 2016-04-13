#ifndef ACCDATADISPLAY_H
#define ACCDATADISPLAY_H

#include <iostream>
#include <QtCharts/QChartView>

QT_CHARTS_USE_NAMESPACE

class AccDataDisplay
{
public:
    AccDataDisplay();
    AccDataDisplay(std::string filePath);
    QChartView *getChartView();
private:
    QChartView *chartView;
};

#endif // ACCDATADISPLAY_H
