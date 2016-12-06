#ifndef APPLICATIONMENUBAR_H
#define APPLICATIONMENUBAR_H

#include <QWidget>
#include <QMenuBar>
#include <QMainWindow>
#include <QShortcut>

class ApplicationMenuBar : public QMenuBar
{
    Q_OBJECT
public:
   ApplicationMenuBar(QWidget *parent = 0);


private:
    QMenu* fichier;
    QMenu* aide;
    QMenu* algorithme;
    QMenu* apropos;
};

#endif // APPLICATIONMENUBAR_H
