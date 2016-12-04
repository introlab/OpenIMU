#ifndef RECORDVIEWWIDGET_H
#define RECORDVIEWWIDGET_H

#include <QWidget>
#include <QLineEdit>
#include "../acquisition/RecordInfo.h"
#include "acquisition/WimuAcquisition.h"
#include "acquisition/WimuRecord.h"
#include "AccDataDisplay.h"
#include "dialogs/FullGraphDialog.h"

namespace Ui {
class RecordViewWidget;
}

class RecordViewWidget : public QWidget
{
    Q_OBJECT

public:
    explicit RecordViewWidget(QWidget *parent = 0);
    RecordViewWidget(QWidget *parent, const WimuAcquisition& data, RecordInfo record);
    ~RecordViewWidget();

public slots:
    void openFullGraphSlot();
    void renameRecord();

public:
    Ui::RecordViewWidget *ui;

    WimuAcquisition acceleroData;
    RecordInfo record;
    bool renameRecordClicked;
    QWidget* m_parent;
    FullGraphDialog *fDialog;

};

#endif // RECORDVIEWWIDGET_H
