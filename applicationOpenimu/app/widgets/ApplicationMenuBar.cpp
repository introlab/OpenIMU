#include "ApplicationMenubar.h"
#include<QGraphicsDropShadowEffect>

ApplicationMenuBar::ApplicationMenuBar(QWidget *parent) : QMenuBar(parent)
{
    this->setPalette(QPalette(Qt::white));

    this->setMinimumWidth(parent->width());
    this->setStyleSheet("color:#2c3e50");

    QGraphicsDropShadowEffect* effect = new QGraphicsDropShadowEffect();
    effect->setBlurRadius(50);
    effect->setYOffset(qreal(-10));
    effect->setXOffset(qreal(-10));
    this->setGraphicsEffect(effect);

    QFont font;
    font.setFamily("Open Sans Light");
    font.setKerning(false);
    font.setPointSize(14);
    this->setFont(font);

    fichier = new QMenu(tr("&Fichier"));
    fichier->setPalette(QPalette(Qt::white));
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
    algorithme->setPalette(QPalette(Qt::white));
    QAction* actionAddAlgo = new QAction(tr("&Ajouter algorithme"),algorithme);
    actionAddAlgo->setShortcut(QKeySequence("Ctrl+D"));
    actionAddAlgo->setEnabled(false);
    algorithme->addAction(actionAddAlgo);

    apropos = new QMenu(tr("&À propos"));
    apropos->setPalette(QPalette(Qt::white));
    QAction* actionAPropos = new QAction(tr("&OpenIMU"),apropos);
    apropos->addAction(actionAPropos);

    aide = new QMenu("&Aide");
    aide->setPalette(QPalette(Qt::white));
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
