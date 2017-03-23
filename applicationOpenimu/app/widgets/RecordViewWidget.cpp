#include "RecordViewWidget.h"
#include "ui_recordviewwidget.h"
#include"../MainWindow.h"

RecordViewWidget::RecordViewWidget(QWidget *parent) :
    QWidget(parent),
    m_ui(new Ui::RecordViewWidget)
{
    m_ui->setupUi(this);
    m_parent = parent;
}

RecordViewWidget::RecordViewWidget(QWidget *parent,  const WimuAcquisition& data, RecordInfo rcd) :
    QWidget(parent),
    m_ui(new Ui::RecordViewWidget)
{
    m_ui->setupUi(this);
    m_parent = parent;
    m_renameRecordClicked = false;
    m_acceleroData = data;
    m_record = rcd;

    m_ui->recordNameEdit->setText(QString::fromStdString(m_record.m_recordName));
    m_ui->recordNameEdit->setStyleSheet("QLineEdit { qproperty-frame: false }");
    m_ui->recordNameEdit->setReadOnly(true);

    if(m_acceleroData.getDates().size()>0)
    {
        m_ui->recordDate->setText(QString::fromStdString(m_acceleroData.getDates().back().date));
    }
    else
    {
        m_ui->recordDate->setText("Enregistrement invalide");
    }

    m_ui->imuType->setText(QString::fromStdString(m_record.m_imuType));
    m_ui->imuPosition->setText(QString::fromStdString(m_record.m_imuPosition));
    m_ui->recordDetails->setText(QString::fromStdString(m_record.m_recordDetails));

    AccDataDisplay *dataDisplay = new AccDataDisplay(m_acceleroData);
    //dataDisplay->showSimplfiedDataDisplay();

    QIcon img(":/icons/edit2.png");
    m_ui->editButton->setIcon(img);
    m_ui->editButton->setIconSize(QSize(15, 15));
    m_ui->graphHorizontalLayout->addWidget(dataDisplay);
    connect(m_ui->fullGraphButton, SIGNAL(clicked()), this, SLOT(openFullGraphSlot()));
    connect(m_ui->algoBtn, SIGNAL(clicked()), parent, SLOT(openAlgorithmTab()));
    connect(m_ui->deleteRecordButton, SIGNAL(clicked()), parent, SLOT(deleteRecord()));

    //** Style
    QIcon imgGraph(":/icons/graphdet.png");
    m_ui->fullGraphButton->setIcon(imgGraph);
    m_ui->fullGraphButton->setIconSize(QSize(157,35));

    QIcon imgAlgo(":/icons/algochoisir.png");
    m_ui->algoBtn->setIcon(imgAlgo);
    m_ui->algoBtn->setIconSize(QSize(157,35));

    //**
    connect(m_ui->editButton, SIGNAL(clicked()), this, SLOT(renameRecord()));

    m_fDialog = new FullGraphDialog();
    m_fDialog->setWindowFlags(windowFlags() | Qt::WindowMinimizeButtonHint);
    m_fDialog->prepareDisplay(m_acceleroData,m_record);
}


RecordViewWidget::~RecordViewWidget()
{
    delete m_ui;
}
void RecordViewWidget::openFullGraphSlot()
{
    if(!m_fDialog->isVisible())
    {
        m_fDialog->show();
    }
}

void RecordViewWidget::renameRecord()
{
    if(!m_renameRecordClicked)
    {
        m_ui->recordNameEdit->setReadOnly(false);
        m_ui->recordNameEdit->setStyleSheet("QLineEdit {qproperty-frame: true }");
        m_renameRecordClicked = true;
        QIcon img(":/icons/check.png");
        m_ui->editButton->setIcon(img);
        m_ui->editButton->setIconSize(QSize(15, 15));

    }
    else
    {
        MainWindow * mainWindow = (MainWindow*)m_parent;
        mainWindow->renameRecordFromUUID(m_record.m_recordId,m_ui->recordNameEdit->text().toStdString());
        m_ui->recordNameEdit->setReadOnly(true);
        m_ui->recordNameEdit->setStyleSheet("QLineEdit {qproperty-frame: false }");
        m_renameRecordClicked = false;
        QIcon img(":/icons/edit2.png");
        m_ui->editButton->setIcon(img);
        m_ui->editButton->setIconSize(QSize(15, 15));
    }

}
