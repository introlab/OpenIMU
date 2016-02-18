#ifndef EXPLORERTAB_H
#define EXPLORERTAB_H

#include <QTabWidget>

class ExplorerTab : public QTabWidget
{
public:
    ExplorerTab(QWidget *parent);
private:
    QWidget* parent;
};

#endif // EXPLORERTAB_H
