#ifndef WORKERTHREADS_H
#define WORKERTHREADS_H

#include <QThread>
#include "OutputNode.h"

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

//Thread String
class WorkerThreadString : public QThread
{
    Q_OBJECT
public:
    WorkerThreadString(OutputNode<std::string>* outputNode, QList<QString> value)
        {this->outputNode = outputNode;
         foreach(QString str, value){
             this->value.push_back(str.toStdString());
         }
        }
    void run() Q_DECL_OVERRIDE
        {outputNode->Send(value);}
private:
    OutputNode<std::string>* outputNode;
    std::vector<std::string> value;
};

#endif // WORKERTHREADS_H
