#ifndef ABOUT_H
#define ABOUT_H

#include <QDialog>
#include "ui_about.h"

class AboutDialog : public QDialog, public Ui::About {
    Q_OBJECT

public:
    AboutDialog( QWidget * parent = 0);
};

#endif // ABOUT_H
