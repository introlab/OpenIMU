function [dataSenso] = getSensoria(date,subject, conn)
%The link with database is already done
%get acc data and put then in a struct dataAcc.time and dataAcc.Raw
%FOR ONE DAY ONLY!
setdbprefs('DataReturnFormat','cellarray')
disp('Exctracting Sensoria data...');
%% Acc
hw_sensor = 'Sensoria';
sensor = 'Accelerometer';
sqlqueryTime = sqlRequestTime(date, subject, sensor, hw_sensor, 0);
sqlqueryAccX = sqlRequest(date, subject, sensor, hw_sensor, 0, 'AccX');
sqlqueryAccY = sqlRequest(date, subject, sensor, hw_sensor, 1, 'AccY');
sqlqueryAccZ = sqlRequest(date, subject, sensor, hw_sensor, 2, 'AccZ');
sensor = 'Gyrometer';
sqlqueryGyroX = sqlRequest(date, subject, sensor, hw_sensor, 0, 'GyroX');
sqlqueryGyroY = sqlRequest(date, subject, sensor, hw_sensor, 1, 'GyroY');
sqlqueryGyroZ = sqlRequest(date, subject, sensor, hw_sensor, 2, 'GyroZ');
sensor = 'Magnetometer';
sqlqueryMagnetoX = sqlRequest(date, subject, sensor, hw_sensor, 0, 'MagnetoX');
sqlqueryMagnetoY = sqlRequest(date, subject, sensor, hw_sensor, 1, 'MagnetoY');
sqlqueryMagnetoZ = sqlRequest(date, subject, sensor, hw_sensor, 2, 'MagnetoZ');
sensor = 'FSR';
sqlqueryFsrX = sqlRequest(date, subject, sensor, hw_sensor, 0, 'LMeta');
sqlqueryFsrY = sqlRequest(date, subject, sensor, hw_sensor, 1, 'RMeta');
sqlqueryFsrZ = sqlRequest(date, subject, sensor, hw_sensor, 2, 'Heel');

%TIME
dataSensoTime = fetch(conn,sqlqueryTime);
dataSensoTime = cell2mat(arrayfun(@(col) vertcat(dataSensoTime{:, col}), 1:size(dataSensoTime, 2), 'UniformOutput', false));
%convert 8bytes read to 64bytes read as double:
byt8vect = vec2mat(typecast(int8(dataSensoTime),'uint8'),8);
bin64vect = [de2bi(byt8vect(:,1),8), de2bi(byt8vect(:,2),8), de2bi(byt8vect(:,3),8), de2bi(byt8vect(:,4),8), de2bi(byt8vect(:,5),8), de2bi(byt8vect(:,6),8), de2bi(byt8vect(:,7),8), de2bi(byt8vect(:,8),8)];
doubleVect = typecast(uint64(bi2de(bin64vect)), 'double');
%Convert the time to datetime format
dataSenso.time =  datetime(doubleVect, 'convertfrom','posixtime', 'TimeZone', 'America/New_York','Format','d-MMM-y HH:mm:ss.SSSS');
clear byt8vect bin64vect doubleVect

%ACC
dataAccPre = [fetch(conn,sqlqueryAccX), fetch(conn,sqlqueryAccY), fetch(conn,sqlqueryAccZ)];
%convert 8bytes read to 32bytes read as single:
dataAccPre = cell2mat(arrayfun(@(col) vertcat(dataAccPre{:, col}), 1:size(dataAccPre, 2), 'UniformOutput', false));
for i = 1:size(dataAccPre,2)
    byt4vect = vec2mat(typecast(int8(dataAccPre(:,i)),'uint8'),4);
    bin32vect = [de2bi(byt4vect(:,1),8), de2bi(byt4vect(:,2),8), de2bi(byt4vect(:,3),8), de2bi(byt4vect(:,4),8)];
    dataSenso.accelerometer(:,i) = typecast(uint32(bi2de(bin32vect)), 'single');
    clear byt4vect bin32vect
end

%GYRO
dataGyroPre = [fetch(conn,sqlqueryGyroX), fetch(conn,sqlqueryGyroY), fetch(conn,sqlqueryGyroZ)];
%convert 8bytes read to 32bytes read as single:
dataGyroPre = cell2mat(arrayfun(@(col) vertcat(dataGyroPre{:, col}), 1:size(dataGyroPre, 2), 'UniformOutput', false));
for i = 1:size(dataGyroPre,2)
    byt4vect = vec2mat(typecast(int8(dataGyroPre(:,i)),'uint8'),4);
    bin32vect = [de2bi(byt4vect(:,1),8), de2bi(byt4vect(:,2),8), de2bi(byt4vect(:,3),8), de2bi(byt4vect(:,4),8)];
    dataSenso.gyroscope(:,i) = typecast(uint32(bi2de(bin32vect)), 'single');
    clear byt4vect bin32vect
end

%Magneto
dataMagnetoPre = [fetch(conn,sqlqueryMagnetoX), fetch(conn,sqlqueryMagnetoY), fetch(conn,sqlqueryMagnetoZ)];
%convert 8bytes read to 32bytes read as single:
dataMagnetoPre = cell2mat(arrayfun(@(col) vertcat(dataMagnetoPre{:, col}), 1:size(dataMagnetoPre, 2), 'UniformOutput', false));
for i = 1:size(dataMagnetoPre,2)
    byt4vect = vec2mat(typecast(int8(dataMagnetoPre(:,i)),'uint8'),4);
    bin32vect = [de2bi(byt4vect(:,1),8), de2bi(byt4vect(:,2),8), de2bi(byt4vect(:,3),8), de2bi(byt4vect(:,4),8)];
    dataSenso.magnetometer(:,i) = typecast(uint32(bi2de(bin32vect)), 'single');
    clear byt4vect bin32vect
end

%FSR
dataFSRPre = [fetch(conn,sqlqueryFsrX), fetch(conn,sqlqueryFsrY), fetch(conn,sqlqueryFsrZ)];
%convert 8bytes read to 32bytes read as single:
dataFSRPre = cell2mat(arrayfun(@(col) vertcat(dataFSRPre{:, col}), 1:size(dataFSRPre, 2), 'UniformOutput', false));
for i = 1:size(dataFSRPre,2)
    byt4vect = vec2mat(typecast(int8(dataFSRPre(:,i)),'uint8'),4);
    bin32vect = [de2bi(byt4vect(:,1),8), de2bi(byt4vect(:,2),8), de2bi(byt4vect(:,3),8), de2bi(byt4vect(:,4),8)];
    dataSenso.fsr(:,i) = typecast(uint32(bi2de(bin32vect)), 'single');
    clear byt4vect bin32vect
end

%% Erase all values out of the day
indx = not(day(date)==day(dataSenso.time));
dataSenso.time(indx)=[];
dataSenso.accelerometer(indx,:)=[];
dataSenso.gyroscope(indx,:)=[];
dataSenso.magnetometer(indx,:)=[];
dataSenso.fsr(indx,:)=[];

end

