#ifndef VBLABEL_PLUGIN_H
#define VBLABEL_PLUGIN_H

#include <QQmlExtensionPlugin>

class VbLabelPlugin : public QQmlExtensionPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QQmlExtensionInterface")

public:
    void registerTypes(const char *uri);
};

#endif // VBLABEL_PLUGIN_H
