#ifndef TOOLBARVIEW_H
#define TOOLBARVIEW_H

#include <QMenuBar>



class ToolbarView : public QMenuBar
{
public:
    ToolbarView(QWidget *parent);

    QMenu* fichier;
    QMenu* edition;
    QMenu* algorithme;
    QMenu* affichage;
    QMenu* aide;
};

#endif // TOOLBARVIEW_H
