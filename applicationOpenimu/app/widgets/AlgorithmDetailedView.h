#ifndef ALGORITHMDETAILEDVIEW_H
#define ALGORITHMDETAILEDVIEW_H

#include <QGroupBox>
#include <QLabel>
#include <QScrollArea>
#include <QTextEdit>
#include <QWidget>

#include "../algorithm/AlgorithmList.h"
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
    QScrollArea* scrollarea;
    QGroupBox * parametersGroupBox;
    QVBoxLayout * parametersLayout;
    QVBoxLayout * detailsLayout;
    QVBoxLayout * mainLayout;
    QHBoxLayout * subMainLayout;
    QLabel * currentSelectionLabel;
    QLabel * selectedDataLabel;
    QLabel * selectedDataValues;
    QLabel * selectedAlgorithmLabel;
    QLabel * selectedAlgorithmValues;
    QLabel * parametersLabel;
    QLabel * parametersValues;
    QLabel * algorithmDetailsLabel;
    QTextEdit * algorithmDetailsValues;
    MRichTextEdit * richTextEdit;
};

#endif // ALGORITHMDETAILEDVIEW_H
