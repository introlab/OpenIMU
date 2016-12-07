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

    QDoubleValidator *validator = new QDoubleValidator(0.00, 0.50, 2, this);
    validator->setNotation(QDoubleValidator::StandardNotation);
    // Adds every parameter to the Dialog Window.
    foreach(ParameterInfo p, m_algorithmInfo.m_parameters)
    {
        if(p.m_name != "uuid")
        {
            QString parameterText = p.m_name.c_str() + QString::fromStdString(": ") + p.m_description.c_str();
            QLabel * itemLabel = new QLabel(Utilities::capitalizeFirstCharacter(parameterText));
            if(p.m_name == "type")
            {
                QComboBox * itemLine = new QComboBox();
                itemLine->addItem("passe-bas");
                itemLine->addItem("passe-haut");
                itemLine->setValidator(validator);
                parametersLayout->addWidget(itemLine);
            }
            else
            {
                QLineEdit * itemLine = new QLineEdit();
                if(p.m_defaultValue.size() > 1)
                    p.m_defaultValue = p.m_defaultValue.replace(1,1,",");

                itemLine->setPlaceholderText(p.m_defaultValue.c_str());
                itemLine->setValidator(validator);
                parametersLayout->addWidget(itemLine);
            }
            parametersLayout->addWidget(itemLabel);
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
        bool isEmpty = le->text().toStdString().empty();
        qDebug() << "le text courant "<< QString::fromStdString(le->text().toStdString());
        qDebug() << "le text coupé  "<< QString::fromStdString(le->text().toStdString().substr(0,2));
        bool isValid = le->text().toStdString().substr(0,2).compare("0,");

        qDebug() << "isEmpty  =="<< le->text().toStdString().empty();
        qDebug() << "isValid =="<< le->text().toStdString().substr(0,2).compare("0,");
        if( isEmpty || isValid != 0)
        {
            m_algorithmInfo.m_parameters.at(index).m_value =  m_algorithmInfo.m_parameters.at(index).m_defaultValue;
        }
        else
        {
            m_algorithmInfo.m_parameters.at(index).m_value = le->text().toStdString().replace(1,1,".");
        }

        index++;
    }

    foreach(QComboBox* cb, findChildren<QComboBox*>())
    {
        m_algorithmInfo.m_parameters.at(index).m_value = cb->currentText().toStdString();
        index++;
    }


    AlgorithmTab * parentTab = (AlgorithmTab*)m_parent;
    parentTab->setAlgorithm(m_algorithmInfo);
    close();
}
