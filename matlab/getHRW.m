function [dataHR] = getHRW(date,subject, conn)
%The link with database is already done
%get HR data and put then in a struct dataHR.time and dataHR.heartrate
%FOR ONE DAY ONLY!
setdbprefs('DataReturnFormat','cellarray')
disp('Exctracting HRW data...');
%% HR
hw_sensor = 'AppleWatch';
sensor = 'Heartrate';
sqlqueryTime = sqlRequestTime(date, subject, sensor, hw_sensor, 1);
sqlquery = sqlRequest(date, subject, sensor, hw_sensor, 1, 'HR');

%TIME
dataHRTime = fetch(conn,sqlqueryTime);
dataHRTime = cell2mat(arrayfun(@(col) vertcat(dataHRTime{:, col}), 1:size(dataHRTime, 2), 'UniformOutput', false));
%convert 8bytes read to 64bytes read as double:
byt8vect = vec2mat(typecast(int8(dataHRTime),'uint8'),8);
bin64vect = [de2bi(byt8vect(:,1),8), de2bi(byt8vect(:,2),8), de2bi(byt8vect(:,3),8), de2bi(byt8vect(:,4),8), de2bi(byt8vect(:,5),8), de2bi(byt8vect(:,6),8), de2bi(byt8vect(:,7),8), de2bi(byt8vect(:,8),8)];
doubleVect = typecast(uint64(bi2de(bin64vect)), 'double');
%Convert the time to datetime format
dataHR.time =  datetime(doubleVect, 'convertfrom','posixtime', 'TimeZone', 'America/New_York','Format','d-MMM-y HH:mm:ss.SSSS');
clear byt8vect bin64vect doubleVect

%DATA
dataHR.heartrate = fetch(conn,sqlquery);
dataHR.heartrate = cell2mat(arrayfun(@(col) vertcat(dataHR.heartrate{:, col}), 1:size(dataHR.heartrate, 2), 'UniformOutput', false));
dataHR.heartrate = vec2mat(typecast(int8(dataHR.heartrate),'uint8'),1);

%% Erase all values out of the day
indx = not(day(date)==day(dataHR.time));
dataHR.time(indx)=[];
dataHR.heartrate(indx,:)=[];

end

