#include "quickitemoutputnode.h"
#include <QThread>

QuickItemOutputNode::QuickItemOutputNode(): QObject(), OutputNode()
{
}

void QuickItemOutputNode::setValue(QVector<int> value)
{
    this->value = value;
    valueBuf = value.toStdVector();

    WorkerThread *workerThread = new WorkerThread(this, valueBuf);
    QObject::connect(workerThread, &WorkerThread::finished, workerThread, &QObject::deleteLater);
    workerThread->start();
}

