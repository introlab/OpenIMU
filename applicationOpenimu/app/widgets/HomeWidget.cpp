#include"HomeWidget.h"
#include "ui_homewidget.h"
#include <QDesktopServices>

HomeWidget::HomeWidget(QWidget *parent) :
    QWidget(parent),
    m_ui(new Ui::HomeWidget)
{
    m_ui->setupUi(this);
    m_parent = parent;
    connect(m_ui->gitbtn, SIGNAL(clicked()), this, SLOT(openGitLink()));

}

HomeWidget::~HomeWidget()
{
    delete m_ui;
}

void HomeWidget::openGitLink()
{
    QString link = "https://github.com/introlab/OpenIMU";
    QDesktopServices::openUrl(QUrl(link));
}
