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
    QMenu* m_fichier;
    QMenu* m_aide;
    QMenu* m_algorithme;
    QMenu* m_apropos;
};

#endif // APPLICATIONMENUBAR_H
