#ifndef BLOCKPLUGIN_H
#define BLOCKPLUGIN_H

#include <QGenericPlugin>
#include "BlockGenerator.h"

class BlockPlugin : public QGenericPlugin
{
    Q_OBJECT

public:
    BlockPlugin(QObject *parent = 0):QGenericPlugin(parent){generator = new BlockGenerator();}
    ~BlockPlugin(){delete generator;}

    // QGenericPlugin interface
public:
    virtual BlockGenerator *create(const QString &name, const QString &spec){return generator;}

protected:
    BlockGenerator* generator;

};

#endif // BLOCKPLUGIN_H
