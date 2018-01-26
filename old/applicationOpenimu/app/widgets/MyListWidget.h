#include <QListWidget>
#include <QFrame>
#include <QPropertyAnimation>
#include <QStyledItemDelegate>

class MyListWidget : public QListWidget {
    Q_OBJECT
public:
    MyListWidget(QWidget *parent = 0)
        : QListWidget(parent){}
};
