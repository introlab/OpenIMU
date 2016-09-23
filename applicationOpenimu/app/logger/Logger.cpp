#include "Logger.h"

#include <string>
#include <fstream>
#include <iostream>
#include <time.h>

using namespace std;

Logger Logger::m_instance=Logger();

Logger::Logger()
{
    LOG.start("logs.txt");
}

Logger::~Logger()
{
    if(m_instance.active){
        m_instance.close();
    }
}

/* Instance of the Singleton Class
 * For ease of use, we have a macro function LOG that call the instance.
*/
Logger& Logger::Instance()
{
    return m_instance;
}

/* Start function for the Logger
 * logFile is the name of the file you want to create
 * The default folder is the binary_function
*/
void Logger::start(string logFile){
    //Status variables modification
    m_instance.active = true;
    //Open filestream
    m_instance.fileStream.open(logFile.c_str(),fstream::app|fstream::out);
}

/* Write function of the Logger
 * Msg is the message you want to write in the logger
 * Automatically add the timestamp and a break line
*/
void Logger::write(string Msg){
    // current date/time based on current system
    time_t now = time(0);

    // convert now to string form
    char* dt = ctime(&now);
    if (m_instance.fileStream && m_instance.active){
        m_instance.fileStream << dt << "    " << Msg.c_str() << endl;
        }
    else{
        cout << Msg;
    }
}

/* Close function of the logger
 * Automatically called in the Destruction function of the classe (~Logger())
*/
void Logger::close(){
    //Status variables modifications
    m_instance.active = false;
    //Close filestream
    m_instance.fileStream.close();
}


