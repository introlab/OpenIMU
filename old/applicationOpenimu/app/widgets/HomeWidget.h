#ifndef HOMEWIDGET_H
#define HOMEWIDGET_H

#include <QWidget>
#include <QVBoxLayout>
#include <QLabel>
#include <QTextEdit>

namespace Ui
{
    class HomeWidget;
}

class HomeWidget : public QWidget {
    Q_OBJECT

public:
    explicit HomeWidget(QWidget *parent = 0);
    ~HomeWidget();

    Ui::HomeWidget *m_ui;
    QWidget* m_parent;

public slots:
    void openGitLink();

};

#endif
