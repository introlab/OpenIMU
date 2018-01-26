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

signals:

    void updateRecords();

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
    Ui::AccDataDisplay *m_ui;
    DataChart * m_chart;
    ChartView *m_chartView;
    QLineSeries *m_lineseriesX;
    QLineSeries *m_lineseriesY;
    QLineSeries *m_lineseriesZ;
    QLineSeries *m_lineseriesAccNorm;
    QLineSeries *m_lineseriesMovingAverage;

    RangeSlider *m_rSlider;

    std::vector<frame> m_availableData;
    std::vector<frame> m_sliceData;
    DbBlock * m_databaseAccess;
    RecordInfo m_recordInfo;

    double m_rSliderValue;
    double m_lSliderValue;
};

#endif // ACCDATADISPLAY_H
