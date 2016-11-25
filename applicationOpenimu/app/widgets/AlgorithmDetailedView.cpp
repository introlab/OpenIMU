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
    algorithmDetailsValues->setSizePolicy(QSizePolicy::MinimumExpanding,QSizePolicy::Ignored);
    richTextEdit = new MRichTextEdit();

    // -- Setting the layout
    parametersLayout->addWidget(currentSelectionLabel);
    parametersLayout->addWidget(selectedDataLabel);
    parametersLayout->addWidget(selectedDataValues);
    parametersLayout->addWidget(selectedAlgorithmLabel);
    parametersLayout->addWidget(selectedAlgorithmValues);
    parametersLayout->addWidget(parametersLabel);
    parametersLayout->addWidget(parametersValues);

    detailsLayout = new QVBoxLayout();
    detailsLayout->addWidget(algorithmDetailsLabel,0);
    detailsLayout->addWidget(algorithmDetailsValues,1);
    //detailsLayout->addWidget(richTextEdit);

    subMainLayout = new QHBoxLayout();
    subMainLayout->addLayout(parametersLayout,1);
    subMainLayout->addLayout(detailsLayout,1);

    //parametersGroupBox->setLayout(subMainLayout);
    //scrollarea->setWidget(parametersGroupBox);

    mainLayout = new QVBoxLayout();
    mainLayout->addWidget(scrollarea);

    this->setLayout(subMainLayout);
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
    if(algorithmInfo.m_parameters.size() == 0 ||
            ((algorithmInfo.m_parameters.size() == 1) && (algorithmInfo.m_parameters.at(0).m_name == "uuid")))
    {
        parametersValues->setText("Aucun paramètre à entrer pour cet algorithme");
    }
    else
    {
        for(int i=0; i<algorithmInfo.m_parameters.size();i++)
        {
            if(selectedAlgorithm.m_parameters.at(i).m_name != "uuid")
            {
                QString parameterName = QString::fromStdString(selectedAlgorithm.m_parameters.at(i).m_name);
                QString parameterValue = QString::fromStdString(selectedAlgorithm.m_parameters.at(i).m_value);

                QString previousParameters = parametersValues->text();
                parametersValues->setText(previousParameters + parameterName + ": " + parameterValue+ "\n" );
            }
        }
    }
    selectedAlgorithmValues->setText(QString::fromStdString(selectedAlgorithm.m_name));
    algorithmDetailsValues->setText(QString::fromStdString(selectedAlgorithm.m_details));

}
