#ifndef EXPLORERDISPLAY_H
#define EXPLORERDISPLAY_H

#include <QTabWidget>

class ExplorerDisplay : public QTabWidget
{
public:
    ExplorerDisplay(QWidget *parent);
private:
    QWidget* parent;
};

#endif // EXPLORERTAB_H
