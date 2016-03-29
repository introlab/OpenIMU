#include "incrementor_plugin.h"
#include "incrementor.h"

#include <qqml.h>

void IncrementorPlugin::registerTypes(const char *uri)
{
    // @uri blocks.incrementor
    qmlRegisterType<Incrementor>(uri, 1, 0, "Incrementor");
}

