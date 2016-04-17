#ifndef RANGESLIDER_H
#define RANGESLIDER_H

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QSlider>
#include <QHBoxLayout>

class RangeSlider : public QWidget
{
    Q_OBJECT
public:
    explicit RangeSlider(QWidget *parent = 0);
    void setRangeValues(int min, int max);
    void setStartHour(int min);
    void setEndHour(int max);
signals:

public slots:

private:
    QSlider *rightSlider;
    QSlider *leftSlider;
    QLabel * rightLabel;
    QLabel * leftLabel;
    QHBoxLayout* mainLayout;

};

#endif // RANGESLIDER_H
