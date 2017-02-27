#ifndef LOGGER_H
#define LOGGER_H

#include <string>
#include <fstream>
#include <iostream>

using namespace std;
/*To use the logger simply include the Logger.h and call LOG.write("String to log")*/
class Logger
{
public:
    static Logger& Instance();
    void write(string Msg);
    void start(string logFile);
    void close();
private:
    //OPERATOR and stuff
    Logger& operator= (const Logger&){ return *this;}
    Logger (const Logger&){}

    // Instance
    static Logger m_instance;
    //File.txt
    ofstream m_fileStream;

    //Status variables
    bool m_active = false;


    Logger();
    ~Logger();
};

//MACRO for ease of use
#define LOG Logger::Instance()

#endif // LOGGER_H
