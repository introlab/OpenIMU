#include "algorithmdetailedview.h"

AlgorithmDetailedView::AlgorithmDetailedView(QWidget *parent) : QWidget(parent)
{
    // -- Parameter Section
    scrollarea = new QScrollArea();

    parametersGroupBox = new QGroupBox();
    parametersGroupBox->setFixedHeight(250);
    parametersGroupBox->setFlat(true);
    parametersLayout = new QVBoxLayout();

    currentSelectionLabel = new QLabel(tr("Sélection courante"));
    selectedDataLabel = new QLabel(tr("Données sélectionnées: "));
    selectedDataValues = new QLabel(tr(" "));
    selectedAlgorithmLabel = new QLabel(tr("Algorithme sélectionné: "));
    selectedAlgorithmValues = new QLabel(tr(" "));
    parametersLabel = new QLabel(tr("Paramètre(s):"));
    parametersValues = new QLabel(tr(""));
    parametersValues->setWordWrap(true);
    algorithmDetailsLabel = new QLabel(tr("Description détaillée"));
    algorithmDetailsValues = new QTextEdit("");
    algorithmDetailsValues->setReadOnly(true);
    algorithmDetailsValues->setSizePolicy(QSizePolicy::Preferred,QSizePolicy::QSizePolicy::MinimumExpanding);
    richTextEdit = new MRichTextEdit();

    // -- Setting the layout
    parametersLayout->addWidget(currentSelectionLabel);
    parametersLayout->addWidget(selectedDataLabel);
    parametersLayout->addWidget(selectedDataValues);
    parametersLayout->addWidget(selectedAlgorithmLabel);
    parametersLayout->addWidget(selectedAlgorithmValues);
    parametersLayout->addWidget(parametersLabel);
    parametersLayout->addWidget(parametersValues);
    parametersLayout->addWidget(algorithmDetailsLabel);
    parametersLayout->addWidget(algorithmDetailsValues);
    //parametersLayout->addWidget(richTextEdit);
    parametersLayout->setSizeConstraint(QLayout::SetMinAndMaxSize);

    parametersGroupBox->setLayout(parametersLayout);
    scrollarea->setWidget(parametersGroupBox);

    QHBoxLayout* mainLayout = new QHBoxLayout();
    mainLayout->addWidget(scrollarea);
    this->setLayout(mainLayout);
}

void AlgorithmDetailedView::Clear()
{
    selectedDataValues->setText("");
    selectedAlgorithmValues->setText("");
    parametersValues->setText("");
    algorithmDetailsValues->setText("");
}

void AlgorithmDetailedView::setAlgorithm(AlgorithmInfo algorithmInfo, AlgorithmInfo selectedAlgorithm)
{
    if(algorithmInfo.parameters.size() == 0 ||
            ((algorithmInfo.parameters.size() == 1) && (algorithmInfo.parameters.at(0).name == "uuid")))
    {
        parametersValues->setText("Aucun paramètre à entrer pour cet algorithme");
    }
    else
    {
        for(int i=0; i<algorithmInfo.parameters.size();i++)
        {
            if(selectedAlgorithm.parameters.at(i).name != "uuid")
            {
                QString parameterName = QString::fromStdString(selectedAlgorithm.parameters.at(i).name);
                QString parameterValue = QString::fromStdString(selectedAlgorithm.parameters.at(i).value);

                QString previousParameters = parametersValues->text();
                parametersValues->setText(previousParameters + parameterName + ": " + parameterValue+ "\n" );
            }
        }
    }
    selectedAlgorithmValues->setText(QString::fromStdString(selectedAlgorithm.name));
    algorithmDetailsValues->setText(QString::fromStdString(selectedAlgorithm.details));

}
