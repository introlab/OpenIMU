#ifndef ACTIVITYTRACKERRESULTS_H
#define ACTIVITYTRACKERRESULTS_H

#include <QWidget>
#include <QtCharts/QChartView>

#include "../algorithm/AlgorithmOutputInfo.h"

namespace Ui {
class ActivityTrackerResults;
}

class ActivityTrackerResults : public QWidget
{
    Q_OBJECT

public:
    explicit ActivityTrackerResults(QWidget *parent = 0);
    ActivityTrackerResults(QWidget *parent, AlgorithmOutputInfo algoOutput);
    ~ActivityTrackerResults();

private:
    Ui::ActivityTrackerResults *ui;
};

#endif // ACTIVITYTRACKERRESULTS_H
