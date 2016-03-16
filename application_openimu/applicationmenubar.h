#ifndef APPLICATIONMENUBAR_H
#define APPLICATIONMENUBAR_H

#include <QWidget>
#include <QMenuBar>
#include <QMainWindow>

class ApplicationMenuBar : public QMenuBar
{
    Q_OBJECT
public:
   ApplicationMenuBar(QWidget *parent = 0);

signals:

public slots:

private:
    QMenu* fichier;
    QMenu* edition;
    QMenu* algorithme;
    QMenu* affichage;
    QMenu* aide;
};

#endif // APPLICATIONMENUBAR_H
