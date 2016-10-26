#include "FullGraphDialog.h"

FullGraphDialog::FullGraphDialog()
{

}

FullGraphDialog::~ FullGraphDialog()
{

}

FullGraphDialog::FullGraphDialog(WimuAcquisition accData)
{
    this->setMinimumSize(800,710);

    this->setWindowTitle(QWidget::tr("Données brutes"));

     mainLayout = new QVBoxLayout(this);
     AccDataDisplay *dataDisplay = new AccDataDisplay(accData);
     mainLayout->addWidget(dataDisplay);
}
