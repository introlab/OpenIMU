#include "applicationmenubar.h"
#include "widget.h"

ApplicationMenuBar::ApplicationMenuBar(QWidget *parent) : QMenuBar(parent)
{
    parent = parent;
    fichier = new QMenu("Fichier");
    QAction* actionOuvrir = new QAction("Ouvrir",fichier);
    fichier->addAction(actionOuvrir);
    edition = new QMenu("Édition");
    algorithme = new QMenu("Algorithme");
    affichage = new QMenu("Affichage");
    aide = new QMenu("Aide");

    this->addMenu(fichier);
    this->addMenu(edition);
    this->addMenu(algorithme);
    this->addMenu(affichage);
    this->addMenu(aide);

    connect(actionOuvrir, SIGNAL(triggered()), parent, SLOT(openFile()));
}

