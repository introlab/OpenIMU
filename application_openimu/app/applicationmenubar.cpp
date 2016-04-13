#include "applicationmenubar.h"

ApplicationMenuBar::ApplicationMenuBar(QWidget *parent) : QMenuBar(parent)
{
    this->setMinimumWidth(parent->width());
    parent = parent;
    fichier = new QMenu("Fichier");
    QAction* actionOuvrir = new QAction("Ouvrir",fichier);
    QAction* actionQuitter = new QAction("Quitter",fichier);
    fichier->addAction(actionOuvrir);
    fichier->addSeparator();
    fichier->addAction(actionQuitter);
    edition = new QMenu("Édition");
    algorithme = new QMenu("Algorithme");
    QAction* actionNombreDePas = new QAction("Nombre de pas",algorithme);
    algorithme->addAction(actionNombreDePas);
    affichage = new QMenu("Affichage");
    aide = new QMenu("Aide");

    this->addMenu(fichier);
    this->addMenu(edition);
    this->addMenu(algorithme);
    this->addMenu(affichage);
    this->addMenu(aide);

    connect(actionOuvrir, SIGNAL(triggered()), parent, SLOT(openFile()));
    connect(actionNombreDePas, SIGNAL(triggered()), parent, SLOT(computeSteps()));
    connect(actionQuitter,SIGNAL(triggered()),parent,SLOT(closeWindow()));
}

