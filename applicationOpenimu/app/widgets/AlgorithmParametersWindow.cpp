#include "AlgorithmParametersWindow.h"

AlgorithmParametersWindow::AlgorithmParametersWindow()
{
    parametersLayout = new QVBoxLayout(this);
    titleLabel = new QLabel("Paramètre(s)");

    parametersLayout->addWidget(titleLabel);
    this->setLayout(parametersLayout);
}
