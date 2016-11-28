#ifndef OPENIMUBUTTON_H
#define OPENIMUBUTTON_H

#include <QPushButton>

class OpenImuButton : public QPushButton
{
    Q_OBJECT
public:
   OpenImuButton(QWidget *parent = 0){

       this->setStyleSheet( "QPushButton{"
                        "background-color: rgba(119, 160, 175, 0.7);"
                        "border-style: inset;"
                        "border-width: 2px;"
                        "border-radius: 10px;"
                        "border-color: white;"
                        "font: 12px;"
                        "min-width: 10em;"
                        "padding: 6px; }"
                        "QPushButton:pressed { background-color: rgba(70, 95, 104, 0.7);}"
    );
   }
};

#endif //
