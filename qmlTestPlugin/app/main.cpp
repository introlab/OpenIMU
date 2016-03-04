#include <QGuiApplication>
#include <QQmlApplicationEngine>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;
    engine.addImportPath("C:/Users/dror2202/Documents/qmlTestPlugin");
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));

    return app.exec();
}
