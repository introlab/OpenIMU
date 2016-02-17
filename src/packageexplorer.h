#ifndef PACKAGEEXPLORER_H
#define PACKAGEEXPLORER_H

#include <QTreeView>

class PackageExplorer : public QMainWindow
{
    Q_OBJECT
public:
    explicit PackageExplorer(QWidget *parent = 0);


signals:

public slots:

private:
    QTreeView* treeView;

};

#endif // PACKAGEEXPLORER_H
