#include "quickitemoutputnode.h"
#include <QThread>

QuickItemOutputNode::QuickItemOutputNode(): QObject(), OutputNode()
{
}

void QuickItemOutputNode::setValue(int v)
{
    value = v;
    valueBuf = v;

    WorkerThread *workerThread = new WorkerThread(this, valueBuf);
    QObject::connect(workerThread, &WorkerThread::finished, workerThread, &QObject::deleteLater);
    workerThread->start();
}

