clear all
close all
clc
tic
%The sqlite command doesnt work for blob data use Java Database
%Connectivity (JBDC) instead

%% Add JBDC driver (if not already set in default folder, see: https://www.mathworks.com/help/database/ug/sqlite-jdbc-windows.html)
%Download the driver here: https://bitbucket.org/xerial/sqlite-jdbc/downloads/
javaaddpath('sqlite-jdbc-3.23.1.jar')
%Configure the database no need to go in databaseExplorer
dataBase = 'C:\Data\Database.oi';
conn = database('','','','org.sqlite.JDBC',['jdbc:sqlite:' dataBase]);

%% Variables
subject = 'P01';
date = '2019-02-15';
namespace = '01b00000000000002018';

%% Acc
dataAcc = getAccW(date, subject, conn);
toc
dataRawAcc = getRawAccW(date, subject, conn);
toc
%% HR
dataHR = getHRW(date, subject, conn);
toc
%% Gyro
dataGyro = getGyroW(date,subject, conn);
toc
dataRawGyro = getRawGyroW(date,subject, conn);
toc
%% Sensoria
dataSenso = getSensoria(date,subject, conn);
toc
%% Battery
dataBattery = getBatteryW(date,subject, conn);
toc
%% Beacons
dataBeacon = getBeacon(date, subject, namespace, conn);
toc 

%% Close Database
close(conn)
clear conn




