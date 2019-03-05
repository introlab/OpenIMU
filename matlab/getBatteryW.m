function [dataBattery] = getBatteryW(date,subject, conn)
%The link with database is already done
%get Battery data and put then in a struct dataHR.time and dataHR.heartrate
%FOR ONE DAY ONLY!
setdbprefs('DataReturnFormat','cellarray')
disp('Exctracting Battery data...');
%% Battery
hw_sensor = 'AppleWatch';
sensor = 'Battery';
sqlqueryTime = sqlRequestTime(date, subject, sensor, hw_sensor, 0);
sqlquery = sqlRequest(date, subject, sensor, hw_sensor, 0, 'Battery');

%TIME
dataBatteryTime = fetch(conn,sqlqueryTime);
dataBatteryTime = cell2mat(arrayfun(@(col) vertcat(dataBatteryTime{:, col}), 1:size(dataBatteryTime, 2), 'UniformOutput', false));
%convert 8bytes read to 64bytes read as double:
byt8vect = vec2mat(typecast(int8(dataBatteryTime),'uint8'),8);
bin64vect = [de2bi(byt8vect(:,1),8), de2bi(byt8vect(:,2),8), de2bi(byt8vect(:,3),8), de2bi(byt8vect(:,4),8), de2bi(byt8vect(:,5),8), de2bi(byt8vect(:,6),8), de2bi(byt8vect(:,7),8), de2bi(byt8vect(:,8),8)];
doubleVect = typecast(uint64(bi2de(bin64vect)), 'double');
%Convert the time to datetime format
dataBattery.time =  datetime(doubleVect, 'convertfrom','posixtime', 'TimeZone', 'America/New_York','Format','d-MMM-y HH:mm:ss.SSSS');
clear byt8vect bin64vect doubleVect

%DATA
dataBatteryPre = fetch(conn,sqlquery);
dataBatteryPre = cell2mat(arrayfun(@(col) vertcat(dataBatteryPre{:, col}), 1:size(dataBatteryPre, 2), 'UniformOutput', false));
byt4vect = vec2mat(typecast(int8(dataBatteryPre),'uint8'),4);
bin32vect = [de2bi(byt4vect(:,1),8), de2bi(byt4vect(:,2),8), de2bi(byt4vect(:,3),8), de2bi(byt4vect(:,4),8)];
dataBattery.level = typecast(uint32(bi2de(bin32vect)), 'single');

%% Erase all values out of the day
indx = not(day(date)==day(dataBattery.time));
dataBattery.time(indx)=[];
dataBattery.level(indx,:)=[];

end

