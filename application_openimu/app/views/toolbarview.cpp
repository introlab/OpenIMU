#include "toolbarview.h"

ToolbarView::ToolbarView(QObject *parent) : QMenuBar(parent)
{
    parent = parent;
    fichier = new QMenu("Fichier");
    QAction* actionOuvrir = new QAction("Ouvrir",fichier);
    fichier->addAction(actionOuvrir);
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

}
