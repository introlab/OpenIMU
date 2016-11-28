#ifndef ALGORITHMTAB_H
#define ALGORITHMTAB_H

#include "MainWidget.h"
#include "QLabel"
#include "QStandardItemModel"
#include "QTableWidget"
#include "algorithmdetailedview.h"
#include "QMessageBox"
#include "../acquisition/RecordInfo.h"
#include "../algorithm/AlgorithmInfoSerializer.h"
#include "../algorithm/AlgorithmOutputInfoSerializer.h"
#include "../acquisition/CJsonSerializer.h"
#include <QWidget>
#include <QNetworkReply>
#include <QNetworkAccessManager>
#include <QPushButton>
#include <QTextEdit>

#include "../acquisition/RecordInfo.h"

class AlgorithmTab : public QWidget
{
    Q_OBJECT
public:
    explicit AlgorithmTab(QWidget *parent, RecordInfo selectedRecord);
    bool getAlgorithmsFromDB();
    void setAlgorithm(AlgorithmInfo algorithmInfo);
    bool createAlgoRequest();

signals:

public slots:
    void openParametersWindow(const QModelIndex &index);
    void reponseAlgoRecue(QNetworkReply* reply);
    void reponseRecue(QNetworkReply* reply);
    void openResultTab();

private:

    QVBoxLayout * algorithmTabLayout;

    // -- Algorithm List Section
    QLabel * algorithmLabel;
    QTableWidget * algorithmTableWidget;
    QStringList algorithmTableHeaders;
    QGroupBox * algorithmListGroupBox;
    QVBoxLayout * algorithmListLayout;

    // -- Spacer Section
    QGroupBox * spacerGroupBox;

    // -- Parameter Section
    AlgorithmDetailedView * algorithmParameters;


    // -- Result Section
    QPushButton * applyAlgorithm;
    QWidget* m_parent;

    std::string m_uuid;
    int selectedIndexRow;
    AlgorithmInfoSerializer m_algorithmSerializer;
    AlgorithmOutputInfoSerializer m_algorithmOutputSerializer;
    AlgorithmInfo m_selectedAlgorithm;

    RecordInfo m_selectedRecord;

    void removeChildren(QLayout* layout);
};

#endif // ALGORITHMTAB_H
