#ifndef LOGGER_H
#define LOGGER_H

#include <string>
#include <fstream>
#include <iostream>

using namespace std;


class Logger
{
public:
    static Logger& Instance();
    void Write(string Msg);
    void Start(string logFile);
    void Close();
private:
    //OPERATOR and stuff
    Logger& operator= (const Logger&){}
    Logger (const Logger&){}

    // Instance
    static Logger m_instance;
    //File.txt
    ofstream fileStream;

    //Status variables
    bool active = false;


    Logger();
    ~Logger();
};

//MACRO for ease of use
#define LOG Logger::Instance()

#endif // LOGGER_H
