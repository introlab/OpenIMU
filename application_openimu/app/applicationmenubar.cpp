#include "applicationmenubar.h"

//DL - Where is widget.h
//#include "widget.h"

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
    //edition = new QMenu("Édition");
    algorithme = new QMenu("Algorithme");
    QAction* actionNombreDePas = new QAction("Compteur de pas",algorithme);
    algorithme->addAction(actionNombreDePas);
    QAction* actionTempsActif = new QAction("Temps d'activité",algorithme);
    algorithme->addAction(actionTempsActif);
    affichage = new QMenu("Affichage");
    QAction* actionDonneeBrutes = new QAction("Données brutes",affichage);
    affichage->addAction(actionDonneeBrutes);
    aide = new QMenu("Aide");
    QAction* actionAPropos = new QAction("À propos",aide);
    aide->addAction(actionAPropos);
    QAction* actionAide = new QAction("Aide",aide);
    aide->addAction(actionAide);

    this->addMenu(fichier);
    //this->addMenu(edition);
    this->addMenu(affichage);
    this->addMenu(algorithme);
    this->addMenu(aide);

    connect(actionDonneeBrutes, SIGNAL(triggered()), parent, SLOT(displayRawAccData()));
    connect(actionOuvrir, SIGNAL(triggered()), parent, SLOT(openFile()));
    connect(actionNombreDePas, SIGNAL(triggered()), parent, SLOT(computeSteps()));
    connect(actionTempsActif,SIGNAL(triggered()),parent,SLOT(computeActivityTime()));
    connect(actionQuitter,SIGNAL(triggered()),parent,SLOT(closeWindow()));
    connect(actionAPropos,SIGNAL(triggered()),parent,SLOT(openAbout()));
    connect(actionAide,SIGNAL(triggered()),parent,SLOT(openHelp()));
}

