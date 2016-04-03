#ifndef CUSTOMQMLSCENE_H
#define CUSTOMQMLSCENE_H

#include <QWidget>

class CustomQmlScene: public QWidget
{
public:
    CustomQmlScene(std::string filename, QWidget *parent);
};

#endif // CUSTOMQMLSCENE_H
