#include "ApplicationMenubar.h"
#include<QGraphicsDropShadowEffect>

ApplicationMenuBar::ApplicationMenuBar(QWidget *parent) : QMenuBar(parent)
{
    this->setStyleSheet("background-color:rgba(255, 255, 255,1);");

    this->setMinimumWidth(parent->width());

    QGraphicsDropShadowEffect* effect = new QGraphicsDropShadowEffect();
    effect->setBlurRadius(50);
    effect->setYOffset(qreal(-10));
    effect->setXOffset(qreal(-10));
    this->setGraphicsEffect(effect);

    fichier = new QMenu(tr("&Fichier"));

    QAction* actionAjouterEnregistrement = new QAction(tr("&Ajouter Enregistrement"), fichier);
    actionAjouterEnregistrement->setShortcut(QKeySequence("Ctrl+R"));

    QAction* actionOuvrir = new QAction(tr("&Charger Enregistrement"),fichier);
    actionOuvrir->setShortcut(QKeySequence("Ctrl+O"));

    QAction* actionQuitter = new QAction(tr("&Quitter"),fichier);
    actionQuitter->setShortcut(QKeySequence("Ctrl+Q"));

    fichier->addAction(actionAjouterEnregistrement);
    fichier->addAction(actionOuvrir);
    fichier->addSeparator();
    fichier->addAction(actionQuitter);

    algorithme = new QMenu("&Algorithme");
    QAction* actionAddAlgo = new QAction(tr("&Ajouter algorithme"),algorithme);
    actionAddAlgo->setShortcut(QKeySequence("Ctrl+D"));
    actionAddAlgo->setEnabled(false);
    algorithme->addAction(actionAddAlgo);

    apropos = new QMenu(tr("&À propos"));
    QAction* actionAPropos = new QAction(tr("&OpenIMU"),apropos);
    apropos->addAction(actionAPropos);

    aide = new QMenu("&Aide");
    QAction* actionAide = new QAction(tr("&Utilisation"),aide);
    aide->addAction(actionAide);

    this->addMenu(fichier);
    this->addMenu(algorithme);
    this->addMenu(apropos);
    this->addMenu(aide);


    connect(actionOuvrir, SIGNAL(triggered()), parent, SLOT(openFile()));
    connect(actionAjouterEnregistrement, SIGNAL(triggered()), parent, SLOT(openRecordDialog()));
    connect(actionQuitter,SIGNAL(triggered()),parent,SLOT(closeWindow()));
    connect(actionAPropos,SIGNAL(triggered()),parent,SLOT(openAbout()));
    connect(actionAide,SIGNAL(triggered()),parent,SLOT(openHelp()));
}
