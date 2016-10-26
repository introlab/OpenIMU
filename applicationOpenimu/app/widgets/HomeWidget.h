#ifndef HOMEWIDGET_H
#define HOMEWIDGET_H

#include <QWidget>
#include <QVBoxLayout>
#include <QLabel>
#include <QTextEdit>

class HomeWidget : public QWidget {
    Q_OBJECT

public:
    HomeWidget(QWidget *parent):
    QWidget(parent)
    {
        this->setStyleSheet("background-color:rgba(230, 233, 239,0.1);");
        mainLayout = new QVBoxLayout;
        this->setLayout(mainLayout);

        QLabel * homeLabel = new QLabel("Open IMU,logiciel de visualisation et d'analyse pour centrale inertielle");
        homeLabel->setFont(QFont( "Arial", 10, QFont::Bold));
        QPixmap pic("../applicationOpenimu/app/icons/logo.png");
        QPixmap scaled=pic.scaled ( 400, 200, Qt::KeepAspectRatio, Qt::FastTransformation );

        QLabel *label = new QLabel(this);
        label->setMaximumWidth(400);
        label->setPixmap(scaled);
        label->setAlignment(Qt::AlignCenter);


        mainLayout->addWidget(label,Qt::AlignCenter);
        mainLayout->addWidget(homeLabel,Qt::AlignCenter);
        mainLayout->addSpacing(20);
        QLabel *fonctions = new QLabel("Fonctionnalités:");
        fonctions->setFont(QFont( "Arial", 10, QFont::Bold));
        QLabel *fonction1 =  new QLabel("- Acquisition des données brutes");
        QLabel *fonction2 =  new QLabel("- Sauvegarde en base de données MongoDB");
        QLabel *fonction3 =  new QLabel("- Traitement des données brutes");
        QLabel *fonction4 =  new QLabel("- Application d'algorithmes");
        QLabel *fonction5 =  new QLabel("- Présentation des données et des résultats");

        QLabel *release = new QLabel("Notes de version:");
        release->setFont(QFont( "Arial", 10, QFont::Bold));
        QTextEdit* releasete = new QTextEdit();
        QString* notes = new QString("Version 2.0 - 24/10/2010 \n\n- Sauvegarde en base de données \n\n- Application d'algorithmes en python sur les données \n\n"
                                     "- Implémentation de l'algorithme: temps d'activité \n\n- Améliorations de l'interface utilisateur \n\n"
                                     "- Centrale inertielle supportée dans cette version: Wimu");
        releasete->setPlainText(*notes);
        releasete->setReadOnly(true);

        QLabel *version = new QLabel("Version: Release 2.0");

        mainLayout->addWidget(fonctions,Qt::AlignCenter);
        mainLayout->addWidget(fonction1);
        mainLayout->addWidget(fonction2);
        mainLayout->addWidget(fonction3);
        mainLayout->addWidget(fonction4);
        mainLayout->addWidget(fonction5);
        mainLayout->addSpacing(50);
        mainLayout->addWidget(release,Qt::AlignCenter);
        mainLayout->addWidget(releasete);
        mainLayout->addSpacing(50);
        mainLayout->addWidget(version);
        mainLayout->setAlignment(label,Qt::AlignCenter);
        mainLayout->setAlignment(homeLabel,Qt::AlignCenter);
        mainLayout->setAlignment(version,Qt::AlignCenter);
    }
    ~HomeWidget();
    QVBoxLayout* mainLayout;

};

#endif
