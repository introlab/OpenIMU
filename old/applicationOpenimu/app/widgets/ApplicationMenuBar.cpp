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

    m_fichier = new QMenu(tr("&Fichier"));
    m_fichier->setPalette(QPalette(Qt::white));
    QAction* actionAjouterEnregistrement = new QAction(tr("&Ajouter Enregistrement"), m_fichier);
    actionAjouterEnregistrement->setShortcut(QKeySequence("Ctrl+R"));

    QAction* actionOuvrir = new QAction(tr("&Charger Enregistrement"),m_fichier);
    actionOuvrir->setShortcut(QKeySequence("Ctrl+O"));

    QAction* actionQuitter = new QAction(tr("&Quitter"),m_fichier);
    actionQuitter->setShortcut(QKeySequence("Ctrl+Q"));

    m_fichier->addAction(actionAjouterEnregistrement);
    m_fichier->addAction(actionOuvrir);
    m_fichier->addSeparator();
    m_fichier->addAction(actionQuitter);

    m_algorithme = new QMenu("&Algorithme");
    m_algorithme->setPalette(QPalette(Qt::white));
    QAction* actionAddAlgo = new QAction(tr("&Ajouter algorithme"),m_algorithme);
    actionAddAlgo->setShortcut(QKeySequence("Ctrl+D"));
    //actionAddAlgo->setEnabled(false);
    m_algorithme->addAction(actionAddAlgo);

    m_apropos = new QMenu(tr("&À propos"));
    m_apropos->setPalette(QPalette(Qt::white));
    QAction* actionAPropos = new QAction(tr("&OpenIMU"),m_apropos);
    m_apropos->addAction(actionAPropos);

    m_aide = new QMenu("&Aide");
    m_aide->setPalette(QPalette(Qt::white));
    QAction* actionAide = new QAction(tr("&Utilisation"),m_aide);
    m_aide->addAction(actionAide);

    this->addMenu(m_fichier);
    this->addMenu(m_algorithme);
    this->addMenu(m_apropos);
    this->addMenu(m_aide);


    connect(actionOuvrir, SIGNAL(triggered()), parent, SLOT(refreshRecordListWidget()));
    connect(actionAjouterEnregistrement, SIGNAL(triggered()), parent, SLOT(openRecordDialog()));
    connect(actionQuitter,SIGNAL(triggered()),parent,SLOT(closeWindow()));
    connect(actionAPropos,SIGNAL(triggered()),parent,SLOT(openAbout()));
    connect(actionAide,SIGNAL(triggered()),parent,SLOT(openHelp()));
    connect(actionAddAlgo,SIGNAL(triggered()),parent,SLOT(addAlgo()));
}
