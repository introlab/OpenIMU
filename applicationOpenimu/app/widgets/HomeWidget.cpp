#include"HomeWidget.h"
#include "ui_homewidget.h"
#include <QDesktopServices>

HomeWidget::HomeWidget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::HomeWidget)
{
    ui->setupUi(this);
    m_parent = parent;
    connect(ui->gitbtn, SIGNAL(clicked()), this, SLOT(openGitLink()));

}

HomeWidget::~HomeWidget()
{
    delete ui;
}

void HomeWidget::openGitLink()
{
    QString link = "https://github.com/introlab/OpenIMU";
    QDesktopServices::openUrl(QUrl(link));
}
