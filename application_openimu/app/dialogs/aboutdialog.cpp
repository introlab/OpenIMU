#include "aboutdialog.h"

AboutDialog::AboutDialog( QWidget * parent) : QDialog(parent) {

    setupUi(this);

    //Removing Help flag
    Qt::WindowFlags flags = windowFlags();

    Qt::WindowFlags helpFlag = Qt::WindowContextHelpButtonHint;

    flags = flags & (~helpFlag);
    setWindowFlags(flags);
}
