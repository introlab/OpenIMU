#include "AlgorithmParametersDialog.h"
#include "../widgets/AlgorithmTab.h"
#include "../utilities/utilities.h"
#include <QDebug>

AlgorithmParametersDialog::AlgorithmParametersDialog(QWidget * parent, AlgorithmInfo algorithm)
{
    m_parent = parent;
    m_algorithmInfo = algorithm;
    m_titleLabel = new QLabel("Paramètre(s)");
    m_parametersLayout = new QVBoxLayout(this);
    m_parametersLayout->addWidget(m_titleLabel);

    this->setWindowIcon(QIcon(":/icons/logo.ico"));

    QDoubleValidator *validator = new QDoubleValidator(0.00, 0.50, 2, this);
    validator->setNotation(QDoubleValidator::StandardNotation);
    // Adds every parameter to the Dialog Window.
    foreach(ParameterInfo parameterInfo, m_algorithmInfo.m_parameters)
    {
        if(parameterInfo.m_name != "uuid")
        {
            QString parameterText = parameterInfo.m_name.c_str() + QString::fromStdString(": ") + parameterInfo.m_description.c_str();
            QLabel * itemLabel = new QLabel(Utilities::capitalizeFirstCharacter(parameterText));
            m_parametersLayout->addWidget(itemLabel);
            if(parameterInfo.m_name == "type")
            {
                QComboBox * itemLine = new QComboBox();
                itemLine->addItem("passe-bas");
                itemLine->addItem("passe-haut");
                itemLine->setValidator(validator);
                m_parametersLayout->addWidget(itemLine);
            }
            else
            {
                QLineEdit * itemLine = new QLineEdit();
                if(parameterInfo.m_defaultValue.size() > 1)
                    parameterInfo.m_defaultValue = parameterInfo.m_defaultValue.replace(1,1,",");

                itemLine->setPlaceholderText(parameterInfo.m_defaultValue.c_str());
                itemLine->setValidator(validator);
                m_parametersLayout->addWidget(itemLine);
            }
        }
    }

    m_sendParametersButton = new QPushButton("Envoyer");
    m_parametersLayout->addWidget(m_sendParametersButton);
    m_cancelButton = new QPushButton("Annuler");
    m_parametersLayout->addWidget(m_cancelButton);

    connect(m_sendParametersButton, SIGNAL(clicked()), this, SLOT(parametersSetSlot()));
    connect(m_cancelButton, SIGNAL(clicked()), this, SLOT(close()));
    this->setLayout(m_parametersLayout);
}

void AlgorithmParametersDialog::parametersSetSlot()
{
    int index = 0;

    foreach(QLineEdit* lineEdit, findChildren<QLineEdit*>())
    {      
        bool isEmpty = lineEdit->text().toStdString().empty();
        bool isValid = lineEdit->text().toStdString().substr(0,2).compare("0,");

        if( isEmpty || isValid != 0)
        {
            m_algorithmInfo.m_parameters.at(index).m_value =  m_algorithmInfo.m_parameters.at(index).m_defaultValue;
        }
        else
        {
            m_algorithmInfo.m_parameters.at(index).m_value = lineEdit->text().toStdString().replace(1,1,".");
        }

        index++;
    }

    foreach(QComboBox* comboBox, findChildren<QComboBox*>())
    {
        m_algorithmInfo.m_parameters.at(index).m_value = comboBox->currentText().toStdString();
        index++;
    }


    AlgorithmTab * parentTab = (AlgorithmTab*)m_parent;
    parentTab->setAlgorithm(m_algorithmInfo);
    close();
}
