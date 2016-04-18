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

signals:

public slots:

private:
    QMenu* fichier;
    QMenu* algorithme;
    QMenu* vue;
    QMenu* aide;
};

#endif // APPLICATIONMENUBAR_H
