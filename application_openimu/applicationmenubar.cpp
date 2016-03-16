#include "applicationmenubar.h"

ApplicationMenuBar::ApplicationMenuBar(QWidget *parent) : QMenuBar(parent)
{
    fichier = new QMenu("Fichier");
    fichier->addMenu(new QMenu("menu1_SubMenu"));
    edition = new QMenu("Édition");
    algorithme = new QMenu("Algorithme");
    affichage = new QMenu("Affichage");
    aide = new QMenu("Aide");

    this->addMenu(fichier);
    this->addMenu(edition);
    this->addMenu(algorithme);
    this->addMenu(affichage);
    this->addMenu(aide);
}

