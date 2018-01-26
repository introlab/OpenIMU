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
    QWidget* getMainWindow();

signals:

public slots:
    void onClickOpenParametersWindow(const QModelIndex &index);
    void reponseAlgoRecue(QNetworkReply* reply);
    void algoListResponse(QNetworkReply* reply);
    void openResultTab();

private:

    QVBoxLayout * m_algorithmTabLayout;

    // -- Algorithm List Section
    QLabel * m_algorithmLabel;
    QTableWidget * m_algorithmTableWidget;
    QStringList m_algorithmTableHeaders;
    QGroupBox * m_algorithmListGroupBox;
    QVBoxLayout * m_algorithmListLayout;

    // -- Spacer Section
    QGroupBox * m_spacerGroupBox;

    // -- Parameter Section
    AlgorithmDetailedView * m_algorithmParameters;


    // -- Result Section
    QPushButton * m_applyAlgorithm;
    QWidget* m_parent;

    std::string m_uuid;
    int m_selectedIndexRow;
    AlgorithmInfoSerializer m_algorithmSerializer;
    AlgorithmOutputInfoSerializer m_algorithmOutputSerializer;
    AlgorithmInfo m_selectedAlgorithm;

    RecordInfo m_selectedRecord;

    void removeChildren(QLayout* layout);
};

#endif // ALGORITHMTAB_H
