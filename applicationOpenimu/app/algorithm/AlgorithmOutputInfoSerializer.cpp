#include"AlgorithmOutputInfoSerializer.h"

AlgorithmOutputInfoSerializer::AlgorithmOutputInfoSerializer()
{

}

AlgorithmOutputInfoSerializer::~AlgorithmOutputInfoSerializer()
{

}

void AlgorithmOutputInfoSerializer::Serialize(AlgorithmOutputInfo algorithmOutputInfo, std::string& serializedAlgorithmOutputInfo )
{
    qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize()";

     Json::Value jsonAlgorithmOutput(Json::objectValue);

     jsonAlgorithmOutput["date"] = algorithmOutputInfo.m_date;
     jsonAlgorithmOutput["startTime"] = algorithmOutputInfo.m_startTime;
     jsonAlgorithmOutput["endTime"] = algorithmOutputInfo.m_endTime;
     jsonAlgorithmOutput["executionTime"] = algorithmOutputInfo.m_executionTime;
     jsonAlgorithmOutput["measureUnit"] = algorithmOutputInfo.m_measureUnit;
     jsonAlgorithmOutput["value"] = algorithmOutputInfo.m_value;

     jsonAlgorithmOutput["algorithmId"] = algorithmOutputInfo.m_algorithmId;
     jsonAlgorithmOutput["algorithmName"] = algorithmOutputInfo.m_algorithmName;

     Json::Value jsonAlgorithmParametersInfo(Json::arrayValue);

     for(int i = 0; i < algorithmOutputInfo.m_algorithmParameters.size(); i++)
     {
        ParameterInfo p = algorithmOutputInfo.m_algorithmParameters.at(i);
        Json::Value jsonParameter(Json::objectValue);

        jsonParameter["description"] = p.description;
        jsonParameter["name"] = p.name;
        jsonParameter["value"] = p.value;

        jsonAlgorithmParametersInfo.append(jsonParameter);
     }

     jsonAlgorithmOutput["algorithmParameters"] = jsonAlgorithmParametersInfo;

     Json::StyledWriter writer;
     serializedAlgorithmOutputInfo = writer.write(jsonAlgorithmOutput);

     qDebug() << " Serialized AlgorithmOutputInfo: ";
     qDebug() << QString::fromStdString(serializedAlgorithmOutputInfo);
}

void AlgorithmOutputInfoSerializer::Deserialize(std::string& dataToDeserialize)
{
   qDebug() << "AlgorithmOutputInfoSerializer::Deserialize()";

   Json::Value deserializeRoot;
   Json::Reader reader;

   if ( !reader.parse(dataToDeserialize, deserializeRoot) )
   {
       dataToDeserialize = "";
       return;
   }
    /*
    m_algorithmOutput.m_date = root.deserializeRoot("date", "").asString();
    m_algorithmOutput.m_startTime = deserializeRoot.get("startTime", "").asString();
    m_algorithmOutput.m_endTime = deserializeRoot.get("endTime", "").asString();
    m_algorithmOutput.m_executionTime = deserializeRoot.get("executionTime", "").asFloat();
    m_algorithmOutput.m_measureUnit = deserializeRoot.get("measureUnit", "").asString();
    m_algorithmOutput.m_value = deserializeRoot.get("value", "").asInt();
    */

    std::string missingInfos = "Not available in Database";
    m_algorithmOutput.m_value = 0;//deserializeRoot.get("value", "").asInt();
    m_algorithmOutput.m_executionTime = 0;//deserializeRoot.get("executionTime", "").asFloat();
    m_algorithmOutput.m_date = missingInfos;//deserializeRoot.get("date", "").asFloat();
    m_algorithmOutput.m_startTime = missingInfos;//deserializeRoot.get("startTime", "").asFloat();
    m_algorithmOutput.m_endTime = missingInfos;//deserializeRoot.get("endTime", "").asFloat();
    m_algorithmOutput.m_measureUnit = missingInfos;//deserializeRoot.get("measureUnit", "").asFloat();

    qDebug() << "AlgorithmOutputInfoSerializer::Deserialize(): About to Deserialize algorithm Id, Name";
    m_algorithmOutput.m_algorithmId = deserializeRoot.get("algorithmId", "").asString();
    m_algorithmOutput.m_algorithmName = deserializeRoot.get("algorithmName", "").asString();

    qDebug() << "AlgorithmOutputInfoSerializer::Deserialize(): About to Deserialize algorithm Parameters";
    Json::Value serializedParameters = deserializeRoot.get("algorithmParameters", "");
    for(int i =0; i<serializedParameters.size(); i++)
    {
        ParameterInfo p;
        p.name = serializedParameters[i].get("name", "").asString();
        p.value = serializedParameters[i].get("value", "").asString();
        p.description = serializedParameters[i].get("description", "").asString();

        m_algorithmOutput.m_algorithmParameters.push_back(p);
    }
}
