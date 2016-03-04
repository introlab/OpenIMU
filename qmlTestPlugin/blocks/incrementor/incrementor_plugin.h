#ifndef INCREMENTOR_PLUGIN_H
#define INCREMENTOR_PLUGIN_H

#include <QQmlExtensionPlugin>

class IncrementorPlugin : public QQmlExtensionPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QQmlExtensionInterface")

public:
    void registerTypes(const char *uri);
};

#endif // INCREMENTOR_PLUGIN_H
