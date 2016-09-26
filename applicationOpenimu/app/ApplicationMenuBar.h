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
   void setUncheck(QString language);

signals:

public slots:

private:
    QMenu* fichier;
    QMenu* algorithme;
    QMenu* vue;
    QMenu* aide;
    QMenu* preference;
    QMenu* preferenceLangue;

    QAction* actionEnglish;
    QAction* actionFrench;
};

#endif // APPLICATIONMENUBAR_H
