#ifndef BUTTONOBSERVER_H
#define BUTTONOBSERVER_H


class ButtonObserver
{
public:
    ButtonObserver();
    virtual void NotifyClick() = 0;
};

#endif // BUTTONOBSERVER_H
