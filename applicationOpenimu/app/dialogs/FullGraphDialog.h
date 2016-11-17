#ifndef FULLGRAPHDIALOH_H
#define FULLGRAPHDIALOH_H

#include <QDialog>
#include <QVBoxLayout>

#include "../acquisition/WimuAcquisition.h"
#include "../AccDataDisplay.h"

class FullGraphDialog : public QDialog
{
    Q_OBJECT

public:
    FullGraphDialog();
    FullGraphDialog(WimuAcquisition acceleroData, RecordInfo recordInfo);
    ~FullGraphDialog();

private:
    QVBoxLayout *mainLayout;
};

#endif
