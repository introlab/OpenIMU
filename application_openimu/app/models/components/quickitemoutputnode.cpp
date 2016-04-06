#include "quickitemoutputnode.h"
#include <QThread>

QuickItemOutputNode::QuickItemOutputNode(): QObject(), OutputNode()
{
}

void QuickItemOutputNode::setValue(int v[])
{
    for(int i = 0; i<MAX_ARRAY_SIZE; i++)
    {
        value[i] = v[i];
        valueBuf[i] = v[i];
    }

    WorkerThread *workerThread = new WorkerThread(this, valueBuf);
    QObject::connect(workerThread, &WorkerThread::finished, workerThread, &QObject::deleteLater);
    workerThread->start();
}

