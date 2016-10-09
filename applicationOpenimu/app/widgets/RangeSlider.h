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
    void setLeftSliderRange(long long min, long long max);
    void setRightSliderRange(long long min, long long max);
    void setStartHour(long long min);
    void setEndHour(long long max);
signals:

public slots:
    void cppSlot(const QVariant &v);

private:
    QLabel * rightLabel;
    QLabel * leftLabel;
    QHBoxLayout* mainLayout;

};

#endif // RANGESLIDER_H
