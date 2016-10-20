#include "AlgorithmParametersWindow.h"
#include "AlgorithmTab.h"

AlgorithmParametersWindow::AlgorithmParametersWindow(QWidget * parent, std::vector<ParametersInfo> parametersList)
{
    m_parent = parent;
    titleLabel = new QLabel("Paramètre(s)");
    parametersLayout = new QVBoxLayout(this);
    parametersLayout->addWidget(titleLabel);

    // Adds every parameter to the Dialog Window.
    for(int i = 0; i < parametersList.size(); i++)
    {
        QLabel * itemLabel = new QLabel(parametersList.at(i).name.c_str());
        QLineEdit * itemLineEdit = new QLineEdit();

        parametersLayout->addWidget(itemLabel);
        parametersLayout->addWidget(itemLineEdit);
    }

    sendParametersButton = new QPushButton("Envoyer");
    parametersLayout->addWidget(sendParametersButton);

    connect(sendParametersButton, SIGNAL(clicked()), this, SLOT(parametersSetSlot()));
    this->setLayout(parametersLayout);
}

void AlgorithmParametersWindow::parametersSetSlot()
{
   //AlgorithmTab * parentTab = (AlgorithmTab)m_parent;
   // parentTab->setAlgoParameters(AlgorithmInfo info);
}
