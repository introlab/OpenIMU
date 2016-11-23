#ifndef ALGORITHMINFO_H
#define ALGORITHMINFO_H

#include <string>
#include <vector>

struct ParametersInfo
{
    std::string name;
    std::string description;
    std::string value;
};

struct AlgorithmInfo
{
    std::string name;
    std::string author;
    std::string description;
    std::string details;
    std::string id;
    std::vector<ParametersInfo> parameters;
};

#endif // ALGORITHMINFO_H
