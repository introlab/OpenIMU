#include "AlgorithmParametersDialog.h"
#include "../widgets/AlgorithmTab.h"
#include <QDebug>

AlgorithmParametersDialog::AlgorithmParametersDialog(QWidget * parent, AlgorithmInfo algo)
{
    m_parent = parent;
    m_parametersList = algo.parameters;
    titleLabel = new QLabel("Paramètre(s)");
    parametersLayout = new QVBoxLayout(this);
    parametersLayout->addWidget(titleLabel);

    // Adds every parameter to the Dialog Window.
    for(int i = 0; i < m_parametersList.size(); i++)
    {
        QLabel * itemLabel = new QLabel(m_parametersList.at(i).name.c_str());
        QLineEdit * itemLineEdit = new QLineEdit();

        parametersLayout->addWidget(itemLabel);
        parametersLayout->addWidget(itemLineEdit);
    }

    sendParametersButton = new QPushButton("Envoyer");
    parametersLayout->addWidget(sendParametersButton);

    connect(sendParametersButton, SIGNAL(clicked()), this, SLOT(parametersSetSlot()));
    this->setLayout(parametersLayout);
}

void AlgorithmParametersDialog::parametersSetSlot()
{
    int index=0;
    foreach(QLineEdit* le, findChildren<QLineEdit*>()) {
        m_parametersList.at(index).value = le->text().toStdString();
        index++;
    }
   AlgorithmTab * parentTab = (AlgorithmTab*)m_parent;
   parentTab->setAlgoParameters(m_parametersList);

}
