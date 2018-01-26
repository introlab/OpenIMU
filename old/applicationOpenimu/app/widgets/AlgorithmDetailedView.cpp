#include "algorithmdetailedview.h"

AlgorithmDetailedView::AlgorithmDetailedView(QWidget *parent) : QWidget(parent)
{
    // -- Parameter Section
    m_scrollarea = new QScrollArea();

    m_parametersGroupBox = new QGroupBox();
    m_parametersGroupBox->setFixedHeight(250);
    m_parametersGroupBox->setFlat(true);
    m_parametersLayout = new QVBoxLayout();

    m_currentSelectionLabel = new QLabel(tr("Sélection courante"));
    m_selectedDataLabel = new QLabel(tr("Données sélectionnées: "));
    m_selectedDataValues = new QLabel(tr(" "));
    m_selectedAlgorithmLabel = new QLabel(tr("Algorithme sélectionné: "));
    m_selectedAlgorithmValues = new QLabel(tr(" "));
    m_parametersLabel = new QLabel(tr("Paramètre(s):"));
    m_parametersValues = new QLabel(tr(""));
    m_parametersValues->setWordWrap(true);
    m_algorithmDetailsLabel = new QLabel(tr("Description détaillée"));
    m_algorithmDetailsValues = new QTextEdit("");
    m_algorithmDetailsValues->setReadOnly(true);
    m_algorithmDetailsValues->setSizePolicy(QSizePolicy::MinimumExpanding,QSizePolicy::Ignored);
    m_richTextEdit = new MRichTextEdit();

    // -- Setting the layout
    m_parametersLayout->addWidget(m_currentSelectionLabel);
    m_parametersLayout->addWidget(m_selectedDataLabel);
    m_parametersLayout->addWidget(m_selectedDataValues);
    m_parametersLayout->addWidget(m_selectedAlgorithmLabel);
    m_parametersLayout->addWidget(m_selectedAlgorithmValues);
    m_parametersLayout->addWidget(m_parametersLabel);
    m_parametersLayout->addWidget(m_parametersValues);

    m_detailsLayout = new QVBoxLayout();
    m_detailsLayout->addWidget(m_algorithmDetailsLabel,0);
    m_detailsLayout->addWidget(m_algorithmDetailsValues,1);
    //detailsLayout->addWidget(richTextEdit);

    m_subMainLayout = new QHBoxLayout();
    m_subMainLayout->addLayout(m_parametersLayout,1);
    m_subMainLayout->addLayout(m_detailsLayout,1);

    m_mainLayout = new QVBoxLayout();
    m_mainLayout->addWidget(m_scrollarea);

    this->setLayout(m_subMainLayout);
}

void AlgorithmDetailedView::Clear()
{
    m_selectedDataValues->setText("");
    m_selectedAlgorithmValues->setText("");
    m_parametersValues->setText("");
    m_algorithmDetailsValues->setText("");
}

void AlgorithmDetailedView::setAlgorithm(AlgorithmInfo algorithmInfo, AlgorithmInfo selectedAlgorithm)
{
    if(algorithmInfo.m_parameters.size() == 0 ||
            ((algorithmInfo.m_parameters.size() == 1) && (algorithmInfo.m_parameters.at(0).m_name == "uuid")))
    {
        m_parametersValues->setText("Aucun paramètre à entrer pour cet algorithme");
    }
    else
    {
        for(int i=0; i<algorithmInfo.m_parameters.size();i++)
        {
            if(selectedAlgorithm.m_parameters.at(i).m_name != "uuid")
            {
                QString parameterName = Utilities::capitalizeFirstCharacter(QString::fromStdString(selectedAlgorithm.m_parameters.at(i).m_name));
                QString parameterValue = QString::fromStdString(selectedAlgorithm.m_parameters.at(i).m_value);

                QString previousParameters = m_parametersValues->text();
                m_parametersValues->setText(previousParameters + parameterName + ": " + parameterValue+ "\n" );
            }
        }
    }
    m_selectedAlgorithmValues->setText(QString::fromStdString(selectedAlgorithm.m_name));
    m_algorithmDetailsValues->setText(QString::fromStdString(selectedAlgorithm.m_details));

}
