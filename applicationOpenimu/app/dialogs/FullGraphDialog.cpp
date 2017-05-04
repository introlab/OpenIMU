#include "FullGraphDialog.h"
#include "ui_FullGraphDialog.h"
#include <QMainWindow>

FullGraphDialog::FullGraphDialog(QWidget *parent) :
    QDialog(parent),
    m_ui(new Ui::FullGraphDialog)
{
    m_ui->setupUi(this);
    this->setWindowIcon(QIcon(":/icons/logo.ico"));

}

FullGraphDialog::~FullGraphDialog()
{
    delete m_ui;
}

void FullGraphDialog::prepareDisplay(WimuAcquisition acceleroData, RecordInfo recordInfo)
{
    m_dataDisplay = new AccDataDisplay(acceleroData,this);
    m_dataDisplay->setInfo(recordInfo);
    m_dataDisplay->show();
    m_ui->mainLayout->addWidget(m_dataDisplay);
}

AccDataDisplay *FullGraphDialog::getAccDataDisplay()
{
    return m_dataDisplay;
}
