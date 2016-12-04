#include "AlgorithmParametersDialog.h"
#include "../widgets/AlgorithmTab.h"
#include "../utilities/utilities.h"
#include <QDebug>

AlgorithmParametersDialog::AlgorithmParametersDialog(QWidget * parent, AlgorithmInfo algorithm)
{
    m_parent = parent;
    m_algorithmInfo = algorithm;
    titleLabel = new QLabel("Paramètre(s)");
    parametersLayout = new QVBoxLayout(this);
    parametersLayout->addWidget(titleLabel);

    this->setWindowIcon(QIcon(":/icons/logo.ico"));

    // Adds every parameter to the Dialog Window.
    foreach(ParameterInfo p, m_algorithmInfo.m_parameters)
    {
        if(p.m_name != "uuid")
        {
            QString parameterText = p.m_name.c_str() + QString::fromStdString(": ") + p.m_description.c_str();
            QLabel * itemLabel = new QLabel(Utilities::capitalizeFirstCharacter(parameterText));

            QLineEdit * itemLineEdit = new QLineEdit();
            parametersLayout->addWidget(itemLabel);
            parametersLayout->addWidget(itemLineEdit);
            itemLineEdit->setPlaceholderText(p.m_defaultValue.c_str());
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
        m_algorithmInfo.m_parameters.at(index).m_value = le->text().toStdString();
        index++;
    }

    AlgorithmTab * parentTab = (AlgorithmTab*)m_parent;
    parentTab->setAlgorithm(m_algorithmInfo);
    close();
}
