#ifndef WORKERTHREADS_H
#define WORKERTHREADS_H

#include <QThread>
#include "outputnode.h"

//Thread Int
class WorkerThreadInt : public QThread
{
    Q_OBJECT
public:
    WorkerThreadInt(OutputNode<int>* outputNode, std::vector<int> value)
        {this->outputNode = outputNode; this->value = value;}
    void run() Q_DECL_OVERRIDE
        {outputNode->Send(value);}
private:
    OutputNode<int>* outputNode;
    std::vector<int> value;
};

//Thread Double
class WorkerThreadDouble : public QThread
{
    Q_OBJECT
public:
    WorkerThreadDouble(OutputNode<double>* outputNode, std::vector<double> value)
        {this->outputNode = outputNode; this->value = value;}
    void run() Q_DECL_OVERRIDE
        {outputNode->Send(value);}
private:
    OutputNode<double>* outputNode;
    std::vector<double> value;
};

#endif // WORKERTHREADS_H
