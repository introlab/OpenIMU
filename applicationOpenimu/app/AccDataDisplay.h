#ifndef ACCDATADISPLAY_H
#define ACCDATADISPLAY_H

#include <QWidget>
#include <QtCharts/QLineSeries>
#include <QtCharts/QChartView>


#include "../acquisition/WimuAcquisition.h"
#include "widgets/RangeSlider.h"
#include "../graph/DataChart.h"
#include "../graph/ChartView.h"
#include"../acquisition/CJsonSerializer.h"
#include"../acquisition/WimuRecord.h"
#include "../core/components/blockType/DbBlock.h"

namespace Ui {
class AccDataDisplay;
}

class AccDataDisplay : public QWidget
{
    Q_OBJECT

public:
    explicit AccDataDisplay(const WimuAcquisition& accData, QWidget *parent = 0);
    void fillChartSeries();
    void leftSliderValueChanged(double value);
    void rightSliderValueChanged(double value);
    void showSimplfiedDataDisplay();
    void setInfo(RecordInfo recInfo);
    ~AccDataDisplay();

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
    Ui::AccDataDisplay *ui;
    DataChart * chart;
    ChartView *chartView;
    QLineSeries *lineseriesX;
    QLineSeries *lineseriesY;
    QLineSeries *lineseriesZ;
    QLineSeries *lineseriesAccNorm;
    QLineSeries *lineseriesMovingAverage;

    RangeSlider *rSlider;

    std::vector<frame> availableData;
    std::vector<frame> sliceData;
    DbBlock * databaseAccess;
    RecordInfo m_recordInfo;

    double rSliderValue;
    double lSliderValue;
};

#endif // ACCDATADISPLAY_H
