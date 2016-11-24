#include "FullGraphDialog.h"
#include "ui_FullGraphDialog.h"

FullGraphDialog::FullGraphDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::FullGraphDialog)
{
    ui->setupUi(this);
}

FullGraphDialog::~FullGraphDialog()
{
    delete ui;
}

void FullGraphDialog::prepareDisplay(WimuAcquisition acceleroData, RecordInfo recordInfo)
{
    m_dataDisplay = new AccDataDisplay2(acceleroData);
    m_dataDisplay->setInfo(recordInfo);
    ui->mainLayout->addWidget(m_dataDisplay);
}

AccDataDisplay2 *FullGraphDialog::getAccDataDisplay()
{
    return m_dataDisplay;
}
