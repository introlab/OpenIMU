#ifndef TOOLBARVIEW_H
#define TOOLBARVIEW_H

#include <QMenuBar>


class ToolbarView : public QMenuBar
{
public:
    ToolbarView(QObject *parent = 0);
private:
    QMenu* fichier;
    QMenu* edition;
    QMenu* algorithme;
    QMenu* affichage;
    QMenu* aide;
};

#endif // TOOLBARVIEW_H
