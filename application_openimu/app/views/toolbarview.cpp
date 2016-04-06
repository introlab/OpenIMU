#include "toolbarview.h"



ToolbarView::ToolbarView(QWidget *controller)
{
    fichier = new QMenu("Fichier");
    edition = new QMenu("Édition");
    algorithme = new QMenu("Algorithme");
    //QAction* actionNombreDePas = new QAction("Nombre de pas",algorithme);
    //algorithme->addAction(actionNombreDePas);
    affichage = new QMenu("Affichage");
    aide = new QMenu("Aide");

    this->addMenu(fichier);
    this->addMenu(edition);
    this->addMenu(algorithme);
    this->addMenu(affichage);
    this->addMenu(aide);

    //connect(actionOuvrir, SIGNAL(triggered()), controller, SLOT(openFile()));
    //connect(actionNombreDePas, SIGNAL(triggered()), controller, SLOT(computeSteps()));

}
