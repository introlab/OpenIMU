#ifndef RECORDSWIDGET_H
#define RECORDSWIDGET_H

#include <QWidget>
#include <QGridLayout>
#include <string>
#include <QLabel>

#include "acquisition/WimuAcquisition.h"
#include "acquisition/WimuRecord.h"
#include "AccDataDisplay.h"

class RecordsWidget: public QWidget
{
    Q_OBJECT

    public:
    RecordsWidget();
    RecordsWidget(QWidget *parent,WimuAcquisition data, RecordInfo record);

    ~RecordsWidget();

    public slots:
    void openFullGraphSlot();

    private:
    QGridLayout* layout;
    WimuAcquisition acceleroData;
    RecordInfo record;
    QLabel* recordTitle;
    QLabel* recordDate;
    QLabel* imuType;
    QLabel* positionImu;
    QPushButton* seeFullGraphBtn;
    QPushButton* goToNextStep;

};

#endif
