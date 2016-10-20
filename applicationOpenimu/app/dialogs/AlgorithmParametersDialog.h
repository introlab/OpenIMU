#ifndef ALGORITHMPARAMETERSWINDOW_H
#define ALGORITHMPARAMETERSWINDOW_H

#include "QLabel"
#include "QDialog"
#include "QVBoxLayout"
#include <QDebug>
#include <QLineEdit>
#include <QPushButton>
#include "../algorithm/AlgorithmList.h"

class AlgorithmParametersDialog : public QDialog
{
    Q_OBJECT

    public:
        AlgorithmParametersDialog(QWidget * parent, std::vector<ParametersInfo> parametersList);
    public slots:
        void parametersSetSlot();

    private:
        QVBoxLayout * parametersLayout;
        QLabel * titleLabel;
        QPushButton * sendParametersButton;
        QWidget* m_parent;
};

#endif // ALGORITHMPARAMETERSWINDOW_H
