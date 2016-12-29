#ifndef ALGORITHMPARAMETERSWINDOW_H
#define ALGORITHMPARAMETERSWINDOW_H

#include "QLabel"
#include "QDialog"
#include "QVBoxLayout"
#include <QDebug>
#include <QLineEdit>
#include <QPushButton>
#include "../algorithm/AlgorithmInfoSerializer.h"

class AlgorithmParametersDialog : public QDialog
{
    Q_OBJECT

    public:
        AlgorithmParametersDialog(QWidget * parent, AlgorithmInfo algorithm);
    public slots:
        void parametersSetSlot();

    private:
        QVBoxLayout * m_parametersLayout;
        QLabel * m_titleLabel;
        QPushButton * m_sendParametersButton;
        QPushButton * m_cancelButton;
        QWidget* m_parent;
        AlgorithmInfo m_algorithmInfo;
};

#endif // ALGORITHMPARAMETERSWINDOW_H
