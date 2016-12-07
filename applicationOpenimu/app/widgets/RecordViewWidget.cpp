#include "RecordViewWidget.h"
#include "ui_recordviewwidget.h"
#include"../MainWindow.h"

RecordViewWidget::RecordViewWidget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::RecordViewWidget)
{
    ui->setupUi(this);
    m_parent = parent;
}

RecordViewWidget::RecordViewWidget(QWidget *parent,  const WimuAcquisition& data, RecordInfo rcd) :
    QWidget(parent),
    ui(new Ui::RecordViewWidget)
{
    ui->setupUi(this);
    m_parent = parent;
    renameRecordClicked = false;
    acceleroData = data;
    record = rcd;

    ui->recordNameEdit->setText(QString::fromStdString(record.m_recordName));
    ui->recordNameEdit->setStyleSheet("QLineEdit { qproperty-frame: false }");
    ui->recordNameEdit->setReadOnly(true);

    if(acceleroData.getDates().size()>0)
    {
        ui->recordDate->setText(QString::fromStdString(acceleroData.getDates().back().date));
    }
    else
    {
        ui->recordDate->setText("Enregistrement invalide");
    }

    ui->imuType->setText(QString::fromStdString(record.m_imuType));
    ui->imuPosition->setText(QString::fromStdString(record.m_imuPosition));
    ui->recordDetails->setText(QString::fromStdString(record.m_recordDetails));

    AccDataDisplay *dataDisplay = new AccDataDisplay(acceleroData);
    dataDisplay->showSimplfiedDataDisplay();

    QIcon img(":/icons/edit2.png");
    ui->editButton->setIcon(img);
    ui->editButton->setIconSize(QSize(15, 15));
    ui->graphHorizontalLayout->addWidget(dataDisplay);
    connect(ui->fullGraphButton, SIGNAL(clicked()), this, SLOT(openFullGraphSlot()));
    connect(ui->algoBtn, SIGNAL(clicked()), parent, SLOT(openAlgorithmTab()));
    connect(ui->deleteRecordButton, SIGNAL(clicked()), parent, SLOT(deleteRecord()));

    //** Style
    QIcon imgGraph(":/icons/graphdet.png");
    ui->fullGraphButton->setIcon(imgGraph);
    ui->fullGraphButton->setIconSize(QSize(157,35));

    QIcon imgAlgo(":/icons/algochoisir.png");
    ui->algoBtn->setIcon(imgAlgo);
    ui->algoBtn->setIconSize(QSize(157,35));

    //**
    connect(ui->editButton, SIGNAL(clicked()), this, SLOT(renameRecord()));

    fDialog = new FullGraphDialog();
    fDialog->setWindowFlags(windowFlags() | Qt::WindowMinimizeButtonHint);
    fDialog->prepareDisplay(acceleroData,record);
}


RecordViewWidget::~RecordViewWidget()
{
    delete ui;
}
void RecordViewWidget::openFullGraphSlot()
{
    if(!fDialog->isVisible())
    {
        fDialog->show();
    }
}

void RecordViewWidget::renameRecord()
{
    if(!renameRecordClicked)
    {
        ui->recordNameEdit->setReadOnly(false);
        ui->recordNameEdit->setStyleSheet("QLineEdit {qproperty-frame: true }");
        renameRecordClicked = true;
        QIcon img(":/icons/check.png");
        ui->editButton->setIcon(img);
        ui->editButton->setIconSize(QSize(15, 15));

    }
    else
    {
        MainWindow * mainWindow = (MainWindow*)m_parent;
        mainWindow->renameRecordFromUUID(record.m_recordId,ui->recordNameEdit->text().toStdString());
        ui->recordNameEdit->setReadOnly(true);
        ui->recordNameEdit->setStyleSheet("QLineEdit {qproperty-frame: false }");
        renameRecordClicked = false;
        QIcon img(":/icons/edit2.png");
        ui->editButton->setIcon(img);
        ui->editButton->setIconSize(QSize(15, 15));

    }

}
