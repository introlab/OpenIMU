#include"AlgorithmInfoSerializer.h"
#include <QDebug>


AlgorithmInfoSerializer::AlgorithmInfoSerializer()
{

}
AlgorithmInfoSerializer::~AlgorithmInfoSerializer()
{

}
void AlgorithmInfoSerializer::Serialize(AlgorithmInfo algorithmInfo, std::string& output)
{
    qDebug() << "calling AlgorithmInfoSerializer::Serialize(): Serializing AlgorithmInfo";
    Json::Value jsonAlgorithmInfo(Json::objectValue);
    Json::Value jsonAlgorithmParametersInfo(Json::arrayValue);

    qDebug() << "Author " << QString::fromStdString(algorithmInfo.author);

    jsonAlgorithmInfo["author"] = algorithmInfo.author;
    jsonAlgorithmInfo["description"] = algorithmInfo.description;
    jsonAlgorithmInfo["details"] = algorithmInfo.details;
    jsonAlgorithmInfo["id"] = algorithmInfo.id;
    jsonAlgorithmInfo["name"] = algorithmInfo.name;

    qDebug() << "calling AlgorithmInfoSerializer::Serialize(): Serializing AlgorithmInfo: Parameters Info";
    qDebug() << " Number of parameters: " << algorithmInfo.parameters.size();
    for(int i = 0; i < algorithmInfo.parameters.size(); i++)
    {
        qDebug() << "iterating... " ;

       ParameterInfo p = algorithmInfo.parameters.at(i);
       Json::Value jsonParameter(Json::objectValue);

       qDebug() << " Parameter name " << QString::fromStdString(p.name);
       jsonParameter["description"] = p.description;
       jsonParameter["name"] = p.name;
       jsonParameter["value"] = p.value;

       jsonAlgorithmParametersInfo.append(jsonParameter);
    }

    jsonAlgorithmInfo["parametersInfo"] = jsonAlgorithmParametersInfo;

    qDebug() << "calling AlgorithmInfoSerializer::Serialize(): Writing the JSON ";
    Json::StyledWriter writer;
    output = writer.write(jsonAlgorithmInfo);
}

void AlgorithmInfoSerializer::Deserialize(std::string& dataToDeserialize)
{
    Json::Value deserializeRoot;
    Json::Reader reader;

    qDebug() << "calling AlgorithmInfoSerializer::Deserialize()";
    qDebug() << "calling AlgorithmInfoSerializer::Deserialize(): dataToDeserialize: " << QString::fromStdString(dataToDeserialize);
    if ( !reader.parse(dataToDeserialize, deserializeRoot) )
    {
        qDebug() << "calling AlgorithmInfoSerializer::Serialize(): CANT parse data";
        dataToDeserialize = "";
        return;
    }

    qDebug() << "calling AlgorithmInfoSerializer::Serialize(): Data parsed";

    // deserialize primitives
    Json::Value algo = deserializeRoot.get("algorithms", "");
    for ( int index = 0; index < algo.size(); ++index )
    {
        AlgorithmInfo temp;
        temp.name = algo[index].get("name", "").asString();
        temp.id = algo[index].get("id", "").asString();
        temp.author = algo[index].get("author", "").asString();
        temp.description = algo[index].get("description", "").asString();
        temp.details = algo[index].get("details", "").asString();

        Json::Value params = algo[index].get("params", "");
        for ( int indexp = 0; indexp < params.size(); ++indexp )
        {
            ParameterInfo pInfo;
            pInfo.name = params[indexp].get("name", "").asString();
            pInfo.description = params[indexp].get("info", "").asString();
            temp.parameters.push_back(pInfo);
        }

        m_algorithmList.push_back(temp);
    }
    qDebug() << "calling AlgorithmInfoSerializer::Serialize(): Done";
}
