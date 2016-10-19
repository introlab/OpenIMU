#ifndef ALGORITHMPARAMETERSWINDOW_H
#define ALGORITHMPARAMETERSWINDOW_H

#include "QLabel"
#include "QDialog"
#include "QVBoxLayout"

class AlgorithmParametersWindow : public QDialog
{
    public:
        AlgorithmParametersWindow();
    private:
        QVBoxLayout * parametersLayout;
        QLabel * titleLabel;
};

#endif // ALGORITHMPARAMETERSWINDOW_H
