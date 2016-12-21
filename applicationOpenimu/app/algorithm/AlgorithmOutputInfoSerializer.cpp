#include"AlgorithmOutputInfoSerializer.h"

AlgorithmOutputInfoSerializer::AlgorithmOutputInfoSerializer()
{

}

AlgorithmOutputInfoSerializer::~AlgorithmOutputInfoSerializer()
{

}

void AlgorithmOutputInfoSerializer::Serialize(AlgorithmOutputInfo algorithmOutputInfo, std::string& serializedAlgorithmOutputInfo )
{
     Json::Value jsonAlgorithmOutput(Json::objectValue);

     // Serializing the member variables ...
     jsonAlgorithmOutput["resultName"] = algorithmOutputInfo.m_resultName;
     jsonAlgorithmOutput["date"] = algorithmOutputInfo.m_date;
     jsonAlgorithmOutput["startTime"] = algorithmOutputInfo.m_startTime;
     jsonAlgorithmOutput["endTime"] = algorithmOutputInfo.m_endTime;
     jsonAlgorithmOutput["executionTime"] = algorithmOutputInfo.m_executionTime;
     jsonAlgorithmOutput["measureUnit"] = algorithmOutputInfo.m_measureUnit;
     jsonAlgorithmOutput["value"] = algorithmOutputInfo.m_value;

     jsonAlgorithmOutput["recordId"] = algorithmOutputInfo.m_recordId;
     jsonAlgorithmOutput["recordName"] = algorithmOutputInfo.m_recordName;
     jsonAlgorithmOutput["recordImuPosition"] = algorithmOutputInfo.m_recordImuPosition;
     jsonAlgorithmOutput["recordImuType"] = algorithmOutputInfo.m_recordType;

     jsonAlgorithmOutput["algorithmId"] = algorithmOutputInfo.m_algorithmId;
     jsonAlgorithmOutput["algorithmName"] = algorithmOutputInfo.m_algorithmName;

     Json::Value jsonAlgorithmParametersInfo(Json::arrayValue);

     // ... and the Algorithm Parameters
     for(int i = 0; i < algorithmOutputInfo.m_algorithmParameters.size(); i++)
     {
        ParameterInfo parameterInfo = algorithmOutputInfo.m_algorithmParameters.at(i);
        Json::Value jsonParameter(Json::objectValue);

        jsonParameter["description"] = parameterInfo.m_description;
        jsonParameter["name"] = parameterInfo.m_name;
        jsonParameter["value"] = parameterInfo.m_value;
        jsonParameter["defaultValue"] = parameterInfo.m_defaultValue;

        jsonAlgorithmParametersInfo.append(jsonParameter);
     }

     jsonAlgorithmOutput["algorithmParameters"] = jsonAlgorithmParametersInfo;

     // Write the Serialized data in an Output String
     Json::StyledWriter writer;
     serializedAlgorithmOutputInfo = writer.write(jsonAlgorithmOutput);
}

void AlgorithmOutputInfoSerializer::Deserialize(std::string& dataToDeserialize)
{
   Json::Value deserializeRoot;
   Json::Reader reader;

   if ( !reader.parse(dataToDeserialize, deserializeRoot) )
   {
       dataToDeserialize = "";
       return;
   }

    std::string missingInfos = "Not available in Database";
    m_algorithmOutput.m_executionTime = deserializeRoot.get("runtime", "").asFloat();
    m_algorithmOutput.m_date = deserializeRoot.get("runtime_start", "").asString();

    if(deserializeRoot.isMember("dispType"))
    {
        m_algorithmOutput.m_dispType= deserializeRoot.get("dispType", "").asString();
    }
    if(m_algorithmOutput.m_dispType.compare("piechart")==0 || m_algorithmOutput.m_dispType.compare("Numeric value")==0)
    {
        m_algorithmOutput.m_value = deserializeRoot.get("result", "").asInt();
    }

    m_algorithmOutput.m_recordId = deserializeRoot.get("recordId", "").asString();
}

void AlgorithmOutputInfoSerializer::DeserializeList(std::string& dataToDeserialize)
{
   Json::Value deserializeRoot;
   Json::Reader reader;

   if ( !reader.parse(dataToDeserialize, deserializeRoot) )
   {
       dataToDeserialize = "";
       return;
   }

    std::string missingInfos = "Not available in Database";

    for ( int index = 0; index < deserializeRoot.size(); ++index )
    {
        AlgorithmOutputInfo algorithmOutputInfo;
        algorithmOutputInfo.m_resultName = deserializeRoot[index].get("resultName", "").asString();
        algorithmOutputInfo.m_value = deserializeRoot[index].get("value", "").asInt();
        algorithmOutputInfo.m_executionTime = deserializeRoot[index].get("executionTime", "").asFloat();
        algorithmOutputInfo.m_date = deserializeRoot[index].get("date", "").asString();
        algorithmOutputInfo.m_startTime = missingInfos; //deserializeRoot.get("startTime", "").asFloat();
        algorithmOutputInfo.m_endTime = missingInfos; //deserializeRoot.get("endTime", "").asFloat();
        algorithmOutputInfo.m_measureUnit = missingInfos; //deserializeRoot.get("measureUnit", "").asFloat();

        algorithmOutputInfo.m_recordId = deserializeRoot[index].get("recordId", "").asString();
        algorithmOutputInfo.m_recordName = deserializeRoot[index].get("recordName", "").asString();
        algorithmOutputInfo.m_recordImuPosition = deserializeRoot[index].get("recordImuPosition", "").asString();

        if(deserializeRoot[index].isMember("recordImuType"))
        {
             algorithmOutputInfo.m_recordType = deserializeRoot[index].get("recordImuType", "").asString();
        }
        algorithmOutputInfo.m_algorithmId = deserializeRoot[index].get("algorithmId", "").asString();
        algorithmOutputInfo.m_algorithmName = deserializeRoot[index].get("algorithmName", "").asString();

        Json::Value serializedParameters = deserializeRoot[index].get("algorithmParameters", "");

        for(int i =0; i<serializedParameters.size(); i++)
        {
            ParameterInfo parameterInfo;
            parameterInfo.m_name = serializedParameters[i].get("name", "").asString();
            parameterInfo.m_value = serializedParameters[i].get("value", "").asString();
            parameterInfo.m_description = serializedParameters[i].get("description", "").asString();

            algorithmOutputInfo.m_algorithmParameters.push_back(parameterInfo);
        }
        m_algorithmOutputList.push_back(algorithmOutputInfo);
    }

}
