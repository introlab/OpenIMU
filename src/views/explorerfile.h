#ifndef EXPLORERFILE_H
#define EXPLORERFILE_H

#include <QTreeView>

class ExplorerFile: public QTreeView
{
public:
    ExplorerFile(QWidget *parent);
private:
    QWidget* parent;
};

#endif // EXPLORERFILE_H
