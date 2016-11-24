#ifndef RECORDSWIDGET_H
#define RECORDSWIDGET_H

#include <QWidget>
#include <QGridLayout>
#include <string>
#include <QLabel>
#include <QLineEdit>

#include "acquisition/WimuAcquisition.h"
#include "acquisition/WimuRecord.h"
#include "AccDataDisplay2.h"
#include "dialogs/FullGraphDialog.h"
#include"../utils/OpenImuButton.h"

class RecordsWidget: public QWidget
{
    Q_OBJECT

    public:
    RecordsWidget();
    RecordsWidget(QWidget *parent,const WimuAcquisition& data, RecordInfo record);

    ~RecordsWidget();

    public slots:
    void openFullGraphSlot();
    void renameRecord();

    private:
    QGridLayout* layout;
    WimuAcquisition acceleroData;
    RecordInfo record;
    QLineEdit* recordNameEdit;
    QLabel* recordTitle;
    QLabel* recordDate;
    QLabel* imuType;
    QLabel* positionImu;
    QLabel* detailsRecord;
    OpenImuButton* deleteBtn;
    OpenImuButton* seeFullGraphBtn;
    OpenImuButton* goToNextStep;
    FullGraphDialog *fDialog;
    bool renameRecordClicked;
    QWidget* m_parent;
    QPushButton * editRecord;
};

#endif
