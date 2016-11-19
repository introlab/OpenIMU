#include "FullGraphDialog.h"

FullGraphDialog::FullGraphDialog()
{

}

FullGraphDialog::~ FullGraphDialog()
{

}

FullGraphDialog::FullGraphDialog(WimuAcquisition* accData, RecordInfo recInfo)
{
    this->setMinimumSize(800,710);

    this->setWindowTitle(QWidget::tr("Données brutes"));

     mainLayout = new QVBoxLayout(this);
     AccDataDisplay *dataDisplay = new AccDataDisplay(accData);
     dataDisplay->setInfo(recInfo);
     mainLayout->addWidget(dataDisplay);
}
