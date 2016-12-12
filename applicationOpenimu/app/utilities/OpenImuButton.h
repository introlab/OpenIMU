#ifndef OPENIMUBUTTON_H
#define OPENIMUBUTTON_H

#include <QPushButton>

class OpenImuButton : public QPushButton
{
    Q_OBJECT
public:
   OpenImuButton(QWidget *parent = 0){
        setOpenImuStyle();
    }

    OpenImuButton(QString textb){
        this->setText(textb);
        setOpenImuStyle();
    }

    void setOpenImuStyle();

};

#endif //
