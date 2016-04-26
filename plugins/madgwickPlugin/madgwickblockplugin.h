#ifndef MULBLOCKPLUGIN_H
#define MULBLOCKPLUGIN_H

#include <QGenericPlugin>
#include "madgwickblockgenerator.h"

class MadgwickBlockPlugin : public QGenericPlugin
{
    Q_OBJECT
#if QT_VERSION >= 0x050000
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QGenericPluginFactoryInterface" FILE "madgwickblockplugin.json")
#endif // QT_VERSION >= 0x050000

public:
    MadgwickBlockPlugin(QObject *parent = 0){generator = new MadgwickBlockGenerator();}

    // QGenericPlugin interface
public:
    BlockGenerator *create(const QString &name, const QString &spec){return generator;}

private:
    MadgwickBlockGenerator* generator;
};

#if QT_VERSION < 0x050000
Q_EXPORT_PLUGIN2(madgwickblock, GenericPlugin)
#endif // QT_VERSION < 0x050000

#endif // MULBLOCKPLUGIN_H
