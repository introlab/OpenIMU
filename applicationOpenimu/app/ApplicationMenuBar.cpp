#include "ApplicationMenubar.h"

ApplicationMenuBar::ApplicationMenuBar(QWidget *parent) : QMenuBar(parent)
{
    this->setMinimumWidth(parent->width());
    parent = parent;
    fichier = new QMenu("&Fichier");

    QAction* actionAjouterEnregistrement = new QAction("&Ajouter Enregistrement", fichier);
    actionAjouterEnregistrement->setShortcut(QKeySequence("Ctrl+R"));

    QAction* actionOuvrir = new QAction("&Ouvrir Enregistrement",fichier);
    actionOuvrir->setShortcut(QKeySequence("Ctrl+O"));

    QAction* actionQuitter = new QAction("&Quitter",fichier);
    actionQuitter->setShortcut(QKeySequence("Ctrl+Q"));

    fichier->addAction(actionAjouterEnregistrement);
    fichier->addAction(actionOuvrir);
    fichier->addSeparator();
    fichier->addAction(actionQuitter);

    algorithme = new QMenu("Al&gorithme");
    QAction* actionNombreDePas = new QAction("&Compteur de pas",algorithme);
    actionNombreDePas->setShortcut(QKeySequence("Ctrl+C"));
    QAction* actionTempsActif = new QAction("&Temps d'activité",algorithme);
    actionTempsActif->setShortcut(QKeySequence("Ctrl+T"));
    algorithme->addAction(actionNombreDePas);
    algorithme->addAction(actionTempsActif);

    vue = new QMenu("&Vue");
    QAction* actionDonneeBrutes = new QAction("&Données brutes",vue);
    actionDonneeBrutes->setShortcut(QKeySequence("Ctrl+D"));
    vue->addAction(actionDonneeBrutes);

    aide = new QMenu("&Aide");
    QAction* actionAPropos = new QAction("À &propos",aide);
    actionAPropos->setShortcut(QKeySequence("Ctrl+A"));
    QAction* actionAide = new QAction("&Aide",aide);
    actionAide->setShortcut(QKeySequence("Ctrl+H"));
    aide->addAction(actionAPropos);
    aide->addAction(actionAide);

    this->addMenu(fichier);
    this->addMenu(vue);
    this->addMenu(algorithme);
    this->addMenu(aide);

    connect(actionDonneeBrutes, SIGNAL(triggered()), parent, SLOT(displayRawAccData()));
    connect(actionOuvrir, SIGNAL(triggered()), parent, SLOT(openFile()));
    connect(actionAjouterEnregistrement, SIGNAL(triggered()), parent, SLOT(openRecordDialog()));
    connect(actionNombreDePas, SIGNAL(triggered()), parent, SLOT(computeSteps()));
    connect(actionTempsActif,SIGNAL(triggered()),parent,SLOT(computeActivityTime()));
    connect(actionQuitter,SIGNAL(triggered()),parent,SLOT(closeWindow()));
    connect(actionAPropos,SIGNAL(triggered()),parent,SLOT(openAbout()));
    connect(actionAide,SIGNAL(triggered()),parent,SLOT(openHelp()));
}

