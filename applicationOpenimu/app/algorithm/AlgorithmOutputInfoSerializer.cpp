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

     // ------------------------------
     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : Date: " << QString::fromStdString(algorithmOutputInfo.m_date);
     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : Start time: " << QString::fromStdString(algorithmOutputInfo.m_startTime);
     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : End time: " << QString::fromStdString(algorithmOutputInfo.m_endTime);
     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : Execution time: " << algorithmOutputInfo.m_executionTime;
     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : Measurement unit: " << QString::fromStdString(algorithmOutputInfo.m_measureUnit);
     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : Value " << algorithmOutputInfo.m_value;

     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : AlgorithmInfo : name: " << QString::fromStdString(algorithmOutputInfo.m_algorithmInfo.name);
     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : AlgorithmInfo : author: " << QString::fromStdString(algorithmOutputInfo.m_algorithmInfo.author);
     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : AlgorithmInfo : description: " << QString::fromStdString(algorithmOutputInfo.m_algorithmInfo.description);
     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : AlgorithmInfo : details: " << QString::fromStdString(algorithmOutputInfo.m_algorithmInfo.details);


     for(int i = 0; i < algorithmOutputInfo.m_algorithmInfo.parameters.size(); i++)
     {
         ParametersInfo p = algorithmOutputInfo.m_algorithmInfo.parameters.at(i);
         qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : AlgorithmInfo : parameter(s) " << i  << " " + QString::fromStdString(p.name);
         qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : AlgorithmInfo : parameter(s) " << i << " " + QString::fromStdString(p.description);
         qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : AlgorithmInfo : parameter(s) " << i << " " + QString::fromStdString(p.value);
     }

     // ------------------------------

     Json::Value jsonAlgorithmOutput(Json::objectValue);

     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize(): AlgorithmOutputInfo";

     qDebug() << "01";
     jsonAlgorithmOutput["date"] = algorithmOutputInfo.m_date;
     qDebug() << "02";
     jsonAlgorithmOutput["startTime"] = algorithmOutputInfo.m_startTime;
     qDebug() << "03";
     jsonAlgorithmOutput["endTime"] = algorithmOutputInfo.m_endTime;
     qDebug() << "04";
     jsonAlgorithmOutput["executionTime"] = algorithmOutputInfo.m_executionTime;
     qDebug() << "05";
     jsonAlgorithmOutput["measureUnit"] = algorithmOutputInfo.m_measureUnit;
     qDebug() << "06";
     jsonAlgorithmOutput["value"] = algorithmOutputInfo.m_value;
     qDebug() << "07";

     // -----------------------------------------------------------------------

     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize(): AlgorithmOutputInfo : AlgorithmInfo";

     std::string serializedAlgorithmInfo;
     AlgorithmInfoSerializer algorithmInfoSerializer;

     algorithmInfoSerializer.Serialize(algorithmOutputInfo.m_algorithmInfo, serializedAlgorithmInfo);

     qDebug() << "calling AlgorithmOutputInfoSerializer::Serialize() : Writing the JSON";

     jsonAlgorithmOutput["algorithmInfo"] = serializedAlgorithmInfo;

     Json::StyledWriter writer;
     serializedAlgorithmOutputInfo = writer.write(jsonAlgorithmOutput);
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
    m_algorithmOutput.m_date = root.get("date", "").asString();
    m_algorithmOutput.m_startTime = root.get("startTime", "").asString();
    m_algorithmOutput.m_endTime = root.get("endTime", "").asString();
    m_algorithmOutput.m_executionTime = root.get("executionTime", "").asFloat();
    m_algorithmOutput.m_measureUnit = root.get("measureUnit", "").asString();
    m_algorithmOutput.m_value = root.get("value", "").asInt();
    */

    std::string missingInfos = "Not available in Database";
    m_algorithmOutput.m_value = 0;//root.get("result", "").asInt();
    m_algorithmOutput.m_executionTime = 0;//root.get("runtime", "").asFloat();
    m_algorithmOutput.m_date = missingInfos;
    m_algorithmOutput.m_startTime = missingInfos;
    m_algorithmOutput.m_endTime = missingInfos;
    m_algorithmOutput.m_measureUnit = missingInfos;

    qDebug() << "AlgorithmInfoSerializer::Deserialize()";

    AlgorithmInfoSerializer algorithmInfoSerializer;
    algorithmInfoSerializer.Deserialize(deserializeRoot.get("algorithms", "").asString());

    qDebug() << "AlgorithmInfoSerializer::Deserialize(): finished deserializing AlgorithmInfo";

    //TODO: Mado: Regarder avec Remi pour retourner plus dans les results?
    if(algorithmInfoSerializer.m_algorithmList.size() > 0)
    {
        std::vector<AlgorithmInfo> a = algorithmInfoSerializer.m_algorithmList;
        AlgorithmInfo ai = a.at(0);
        qDebug() << "Author: "<< QString::fromStdString(ai.author);
    }

    AlgorithmInfo temp;

    qDebug() << "AlgorithmOutputInfoSerializer::Deserialize(): setting the algorithm";
    m_algorithmOutput.m_algorithmInfo = temp;//algorithmInfoSerializer->m_algorithmList.at(0);
}
