#ifndef ALGORITHMDETAILEDVIEW_H
#define ALGORITHMDETAILEDVIEW_H

#include <QGroupBox>
#include <QLabel>
#include <QScrollArea>
#include <QTextEdit>
#include <QWidget>

#include "../utilities/Utilities.h"
#include "../algorithm/AlgorithmInfoSerializer.h"
#include "MRichTextEditor/mrichtextedit.h"

class AlgorithmDetailedView : public QWidget
{
    Q_OBJECT
public:
    explicit AlgorithmDetailedView(QWidget *parent = 0);
    void Clear();
signals:

public slots:
    void setAlgorithm(AlgorithmInfo algorithmInfo, AlgorithmInfo selectedAlgorithm);

private:
    // -- Parameter Section
    QScrollArea* m_scrollarea;
    QGroupBox * m_parametersGroupBox;
    QVBoxLayout * m_parametersLayout;
    QVBoxLayout * m_detailsLayout;
    QVBoxLayout * m_mainLayout;
    QHBoxLayout * m_subMainLayout;
    QLabel * m_currentSelectionLabel;
    QLabel * m_selectedDataLabel;
    QLabel * m_selectedDataValues;
    QLabel * m_selectedAlgorithmLabel;
    QLabel * m_selectedAlgorithmValues;
    QLabel * m_parametersLabel;
    QLabel * m_parametersValues;
    QLabel * m_algorithmDetailsLabel;
    QTextEdit * m_algorithmDetailsValues;
    MRichTextEdit * m_richTextEdit;
};

#endif // ALGORITHMDETAILEDVIEW_H
