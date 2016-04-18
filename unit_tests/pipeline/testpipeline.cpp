#include "testpipeline.h"

#include "../../application_openimu/app/models/components/block.h"
#include "../../application_openimu/app/models/components/inputnode.h"
#include "../../application_openimu/app/models/components/outputnode.h"
#include "../../application_openimu/app/models/json/json/json.h"
#include "../../application_openimu/app/models/caneva.h"
#include <string>
#include <vector>
#include <QtGlobal>

TestPipeline::TestPipeline(QObject *parent) : QObject(parent)
{
    caneva = new Caneva("../savefiles/test_block_mul.json",0);
}

void TestPipeline::testsJSON()
{
    QFETCH(std::vector<float> , input1);
    QFETCH(std::vector<float> , input2);
    QFETCH(std::vector<float> , result);

    caneva->getBlock("multiplier")->GetInput<float>("input1")->Put(input1);
    caneva->getBlock("multiplier")->GetInput<float>("input2")->Put(input2);
    std::vector<float> calculated = caneva->getBlock("multiplier")->GetOutput<float>("output1")->getValueBuf();

    unsigned int minSize = std::min(std::min(input1.size(),input2.size()), calculated.size());
    for(int i = 0; i<minSize; i++)
        qFuzzyCompare(calculated[i],result[i]);
}

void TestPipeline::testsJSON_data()
{
    QTest::addColumn<std::vector<float> >("input1");
    QTest::addColumn<std::vector<float> >("input2");
    QTest::addColumn<std::vector<float> >("result");

    QTest::newRow("1") << std::vector<float>({1.1,2.2,3.3}) // input1
                       << std::vector<float>({1.1,2.2,3.3}) // input2
                       << std::vector<float>({1.21,4.84,10.89}); // output

    QTest::newRow("2") << std::vector<float>({-1.1,-2.2,-3.3}) // input1
                       << std::vector<float>({1.1,2.2,3.3}) // input2
                       << std::vector<float>({-1.21,-4.84,-10.89}); // output

    QTest::newRow("3") << std::vector<float>({-1.1,-2.2,-3.3}) // input1
                       << std::vector<float>({-1.1,-2.2,-3.3}) // input2
                       << std::vector<float>({1.21,4.84,10.89}); // output


    QTest::newRow("4") << std::vector<float>({1,2,3}) // input1
                       << std::vector<float>({0,0,0}) // input2
                       << std::vector<float>({0,0,0}); // output
}
