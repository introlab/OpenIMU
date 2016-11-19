#include "AlgorithmParametersDialog.h"
#include "../widgets/AlgorithmTab.h"
#include "../utils/Utils.h"
#include <QDebug>

AlgorithmParametersDialog::AlgorithmParametersDialog(QWidget * parent, AlgorithmInfo algorithm)
{
    m_parent = parent;
    m_algorithmInfo = algorithm;
    titleLabel = new QLabel("Paramètre(s)");
    parametersLayout = new QVBoxLayout(this);
    parametersLayout->addWidget(titleLabel);

    // Adds every parameter to the Dialog Window.
    foreach(ParametersInfo p, m_algorithmInfo.parameters)
    {
        if(p.name != "uuid")
        {
            QString parameterText = p.name.c_str() + QString::fromStdString(": ") + p.description.c_str();
            QLabel * itemLabel = new QLabel(Utils::capitalizeFirstCharacter(parameterText));

            QLineEdit * itemLineEdit = new QLineEdit();

            parametersLayout->addWidget(itemLabel);
            parametersLayout->addWidget(itemLineEdit);
        }
    }

    sendParametersButton = new QPushButton("Envoyer");
    parametersLayout->addWidget(sendParametersButton);
    cancelButton = new QPushButton("Annuler");
    parametersLayout->addWidget(cancelButton);

    connect(sendParametersButton, SIGNAL(clicked()), this, SLOT(parametersSetSlot()));
    connect(cancelButton, SIGNAL(clicked()), this, SLOT(close()));
    this->setLayout(parametersLayout);
}

void AlgorithmParametersDialog::parametersSetSlot()
{
    int index = 0;

    foreach(QLineEdit* le, findChildren<QLineEdit*>())
    {
        m_algorithmInfo.parameters.at(index).value = le->text().toStdString();
        index++;
    }

    AlgorithmTab * parentTab = (AlgorithmTab*)m_parent;
    parentTab->setAlgorithm(m_algorithmInfo);
    close();
}
