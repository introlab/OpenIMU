#ifndef ALGORITHMTAB_H
#define ALGORITHMTAB_H

#include "MainWidget.h"
#include "QLabel"
#include "QStandardItemModel"
#include "QTableWidget"
#include "../algorithm/AlgorithmList.h"
#include "../acquisition/CJsonSerializer.h"

#include <QWidget>
#include <QNetworkReply>
#include <QNetworkAccessManager>
#include <QPushButton>

class AlgorithmTab : public QWidget
{
    Q_OBJECT
public:
    explicit AlgorithmTab(QWidget *parent, std::string uuid);
    bool getAlgorithmsFromDB();
signals:

public slots:
    void openParametersWindow(const QModelIndex &index);
    void reponseRecue(QNetworkReply* reply);
    void openResultTab();

private:
    QVBoxLayout * algorithmLayout;

    // -- Algorithm List Section
    QLabel * algorithmLabel;
    QTableWidget * algorithmTableWidget;
    QStringList algorithmTableHeaders;

    // -- Parameter Section
    QLabel * parameterLabel;

    QLabel * parameterValues;

    // -- Result Section
    QPushButton * applyAlgorithm;
    QWidget* m_parent;

    std::string m_uuid;
    AlgorithmList algoList;
};

#endif // ALGORITHMTAB_H
