#ifndef HELP_H
#define HELP_H

#include <QDialog>
#include "ui_help.h"

class HelpDialog : public QDialog, public Ui::Help {
    Q_OBJECT

public:
    HelpDialog( QWidget * parent = 0);
};

#endif // HELP_H
