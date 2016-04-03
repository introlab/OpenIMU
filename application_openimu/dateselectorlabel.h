#ifndef DATESELECTORLABEL_H
#define DATESELECTORLABEL_H

#include <qlabel.h>

class DateSelectorLabel: public QLabel
{
Q_OBJECT
public:
    explicit DateSelectorLabel( const QString& text="", QWidget* parent=0 );
    ~DateSelectorLabel();
signals:
    void clicked(std::string text);
protected:
    void mousePressEvent(QMouseEvent* event);
private:
    std::string fullPath;
};

#endif // DATESELECTORLABEL_H
