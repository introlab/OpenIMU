#ifndef MULBLOCKPLUGIN_H
#define MULBLOCKPLUGIN_H

#include <QGenericPlugin>
#include "mulblockgenerator.h"

class MulBlockPlugin : public QGenericPlugin
{
    Q_OBJECT
#if QT_VERSION >= 0x050000
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QGenericPluginFactoryInterface" FILE "mulblockplugin.json")
#endif // QT_VERSION >= 0x050000

public:
    MulBlockPlugin(QObject *parent = 0){generator = new MulBlockGenerator();}

    // QGenericPlugin interface
public:
    BlockGenerator *create(const QString &name, const QString &spec){return generator;}

private:
    MulBlockGenerator* generator;
};

#if QT_VERSION < 0x050000
Q_EXPORT_PLUGIN2(mulblock, GenericPlugin)
#endif // QT_VERSION < 0x050000

#endif // MULBLOCKPLUGIN_H
