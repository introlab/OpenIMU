function [dataAcc] = getRawAccW(date,subject, conn)
%The link with database is already done
%get acc data and put then in a struct dataAcc.time and dataAcc.Raw
%FOR ONE DAY ONLY!
setdbprefs('DataReturnFormat','cellarray')
disp('Exctracting RawAccW data...');
%% Acc
hw_sensor = 'AppleWatch';
sensor = 'Raw Accelerometer';
sqlqueryTime = sqlRequestTime(date, subject, sensor, hw_sensor, 0);
sqlqueryX = sqlRequest(date, subject, sensor, hw_sensor, 0, 'AccX');
sqlqueryY = sqlRequest(date, subject, sensor, hw_sensor, 1, 'AccY');
sqlqueryZ = sqlRequest(date, subject, sensor, hw_sensor, 2, 'AccZ');

%TIME
dataAccTime = fetch(conn,sqlqueryTime);
dataAccTime = cell2mat(arrayfun(@(col) vertcat(dataAccTime{:, col}), 1:size(dataAccTime, 2), 'UniformOutput', false));
%convert 8bytes read to 64bytes read as double:
byt8vect = vec2mat(typecast(int8(dataAccTime),'uint8'),8);
bin64vect = [de2bi(byt8vect(:,1),8), de2bi(byt8vect(:,2),8), de2bi(byt8vect(:,3),8), de2bi(byt8vect(:,4),8), de2bi(byt8vect(:,5),8), de2bi(byt8vect(:,6),8), de2bi(byt8vect(:,7),8), de2bi(byt8vect(:,8),8)];
doubleVect = typecast(uint64(bi2de(bin64vect)), 'double');
%Convert the time to datetime format
dataAcc.time =  datetime(doubleVect, 'convertfrom','posixtime', 'TimeZone', 'America/New_York','Format','d-MMM-y HH:mm:ss.SSSS');
clear byt8vect bin64vect doubleVect

%ACC
dataAccPre = [fetch(conn,sqlqueryX), fetch(conn,sqlqueryY), fetch(conn,sqlqueryZ)];
%convert 8bytes read to 32bytes read as single:
dataAccPre = cell2mat(arrayfun(@(col) vertcat(dataAccPre{:, col}), 1:size(dataAccPre, 2), 'UniformOutput', false));
for i = 1:size(dataAccPre,2)
    byt4vect = vec2mat(typecast(int8(dataAccPre(:,i)),'uint8'),4);
    bin32vect = [de2bi(byt4vect(:,1),8), de2bi(byt4vect(:,2),8), de2bi(byt4vect(:,3),8), de2bi(byt4vect(:,4),8)];
    dataAcc.Raw(:,i) = typecast(uint32(bi2de(bin32vect)), 'single');
    clear byt4vect bin32vect
end

%% Erase all values out of the day
indx = not(day(date)==day(dataAcc.time));
dataAcc.time(indx)=[];
dataAcc.Raw(indx,:)=[];

end

