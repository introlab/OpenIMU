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
        ParameterInfo p = algorithmOutputInfo.m_algorithmParameters.at(i);
        Json::Value jsonParameter(Json::objectValue);

        jsonParameter["description"] = p.m_description;
        jsonParameter["name"] = p.m_name;
        jsonParameter["value"] = p.m_value;
        jsonParameter["defaultValue"] = p.m_defaultValue;

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
    m_algorithmOutput.m_resultName = deserializeRoot.get("resultName", "").asString();
    m_algorithmOutput.m_value = deserializeRoot.get("result", "").asInt();

    m_algorithmOutput.m_executionTime = deserializeRoot.get("runtime", "").asFloat();

    m_algorithmOutput.m_date = deserializeRoot.get("runtime_start", "").asString();
    m_algorithmOutput.m_startTime = missingInfos;//deserializeRoot.get("startTime", "").asFloat();
    m_algorithmOutput.m_endTime = missingInfos;//deserializeRoot.get("endTime", "").asFloat();
    m_algorithmOutput.m_measureUnit = missingInfos;//deserializeRoot.get("measureUnit", "").asFloat();

    m_algorithmOutput.m_recordId = deserializeRoot.get("recordId", "").asString();
    m_algorithmOutput.m_recordName = deserializeRoot.get("recordName", "").asString();
    m_algorithmOutput.m_recordImuPosition = deserializeRoot.get("recordImuPosition", "").asString();
    m_algorithmOutput.m_recordType = deserializeRoot.get("recordImuType", "").asString();
    m_algorithmOutput.m_algorithmId = deserializeRoot.get("algorithmId", "").asString();
    m_algorithmOutput.m_algorithmName = deserializeRoot.get("algorithmName", "").asString();

    Json::Value serializedParameters = deserializeRoot.get("algorithmParameters", "");
    for(int i =0; i<serializedParameters.size(); i++)
    {
        ParameterInfo p;
        p.m_name = serializedParameters[i].get("name", "").asString();
        p.m_value = serializedParameters[i].get("value", "").asString();
        p.m_defaultValue = serializedParameters[i].get("defaultValue", "").asString();
        p.m_description = serializedParameters[i].get("description", "").asString();

        m_algorithmOutput.m_algorithmParameters.push_back(p);
    }
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
        AlgorithmOutputInfo temp;
        temp.m_resultName = deserializeRoot[index].get("resultName", "").asString();
        temp.m_value = deserializeRoot[index].get("value", "").asInt();
        temp.m_executionTime = deserializeRoot[index].get("executionTime", "").asFloat();
        temp.m_date = deserializeRoot[index].get("date", "").asString();
        temp.m_startTime = missingInfos; //deserializeRoot.get("startTime", "").asFloat();
        temp.m_endTime = missingInfos; //deserializeRoot.get("endTime", "").asFloat();
        temp.m_measureUnit = missingInfos; //deserializeRoot.get("measureUnit", "").asFloat();

        temp.m_recordId = deserializeRoot[index].get("recordId", "").asString();
        temp.m_recordName = deserializeRoot[index].get("recordName", "").asString();
        temp.m_recordImuPosition = deserializeRoot[index].get("recordImuPosition", "").asString();

        if(deserializeRoot[index].isMember("recordImuType"))
        {
             temp.m_recordType = deserializeRoot[index].get("recordImuType", "").asString();
        }
        temp.m_algorithmId = deserializeRoot[index].get("algorithmId", "").asString();
        temp.m_algorithmName = deserializeRoot[index].get("algorithmName", "").asString();

        Json::Value serializedParameters = deserializeRoot[index].get("algorithmParameters", "");

        for(int i =0; i<serializedParameters.size(); i++)
        {
            ParameterInfo p;
            p.m_name = serializedParameters[i].get("name", "").asString();
            p.m_value = serializedParameters[i].get("value", "").asString();
            p.m_description = serializedParameters[i].get("description", "").asString();

            temp.m_algorithmParameters.push_back(p);
        }
        m_algorithmOutputList.push_back(temp);
    }

}
