#include "vblabel_plugin.h"
#include "vblabel.h"

#include <qqml.h>

void VbLabelPlugin::registerTypes(const char *uri)
{
    // @uri blocks.visual.label
    qmlRegisterType<VBLabel>(uri, 1, 0, "VBLabel");
}

