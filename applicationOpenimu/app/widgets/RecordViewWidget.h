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
    RecordViewWidget(QWidget *parent, const WimuAcquisition& data, RecordInfo m_record);
    ~RecordViewWidget();

public slots:
    void openFullGraphSlot();
    void renameRecord();

public:
    Ui::RecordViewWidget *m_ui;

    WimuAcquisition m_acceleroData;
    RecordInfo m_record;
    bool m_renameRecordClicked;
    QWidget* m_parent;
    FullGraphDialog *m_fDialog;

};

#endif // RECORDVIEWWIDGET_H
