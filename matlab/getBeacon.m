function [dataBeacon] = getBeacon(date, subject, namespace, conn)
%Function return a struc where all beacons present in namespace are listed 
disp('Exctracting Beacon data...');
%Start to list all beacons in namespace
hw_sensor = 'Kontact';
sensor = 'Beacons';
% namespace = '01b00000000000002018';
setdbprefs('DataReturnFormat','cellarray')
sqlquery = [...
    'SELECT tabChannels.label '...
    'FROM tabChannels '...
    'WHERE tabChannels.id_sensor = ('...
        'SELECT tabSensors.id_sensor '...
        'FROM tabSensors '...
        'WHERE tabSensors.name = ''Beacons'' '...
        'AND  tabSensors.hw_name = ''Kontact'''...
        ')'...
    ];
beaconlist = fetch(conn,sqlquery);
listUnique = cell2mat(unique(cellfun(@(x) replace(x,{'_TxPower', '_RSSI'},''),beaconlist,'uni',0)));
%Keep only the ones in the good namespace
listUnique(~strcmp(string(listUnique(:,[1:20])), namespace),:)=[];
instanceID = string(listUnique(:,[22:33]));

%Create the struct for each beacon
for i = 1:length(instanceID)
    label = strcat([namespace '_' char(instanceID(i)) '_TxPower']);
    sqlqueryTx = sqlRequestBeacon(date, subject, sensor, hw_sensor, label, 'TxPower');
    beaconPreTx = fetch(conn,sqlqueryTx);
    label = strcat([namespace '_' char(instanceID(i)) '_RSSI']);
    sqlqueryRSSI = sqlRequestBeacon(date, subject, sensor, hw_sensor, label, 'RSSI');
    beaconPreRSSI = fetch(conn,sqlqueryRSSI);
    sqlqueryTime = sqlRequestBeaconTime(date, subject, sensor, hw_sensor, label);
    beaconPreTime = fetch(conn,sqlqueryTime);
    if ~isempty(beaconPreTx)
        beaconPreTime = cell2mat(arrayfun(@(col) vertcat(beaconPreTime{:, col}), 1:size(beaconPreTime, 2), 'UniformOutput', false));
        byt8vect = vec2mat(typecast(int8(beaconPreTime),'uint8'),8);
        bin64vect = [de2bi(byt8vect(:,1),8), de2bi(byt8vect(:,2),8), de2bi(byt8vect(:,3),8), de2bi(byt8vect(:,4),8), de2bi(byt8vect(:,5),8), de2bi(byt8vect(:,6),8), de2bi(byt8vect(:,7),8), de2bi(byt8vect(:,8),8)];
        doubleVect = typecast(uint64(bi2de(bin64vect)), 'double');
        %Convert the time to datetime format
        dataBeacon.(strcat('B_', instanceID(i))).time =  datetime(doubleVect, 'convertfrom','posixtime', 'TimeZone', 'America/New_York','Format','d-MMM-y HH:mm:ss.SSSS');
        %Export all variables
        dataBeacon.(strcat('B_', instanceID(i))).TxPower = cell2mat(arrayfun(@(col) vertcat(beaconPreTx{:, col}), 1:size(beaconPreTx, 2), 'UniformOutput', false));
        dataBeacon.(strcat('B_', instanceID(i))).RSSI = cell2mat(arrayfun(@(col) vertcat(beaconPreRSSI{:, col}), 1:size(beaconPreRSSI, 2), 'UniformOutput', false));
        dataBeacon.(strcat('B_', instanceID(i))).namespace = namespace;
        dataBeacon.(strcat('B_', instanceID(i))).instanceID = instanceID(i);
    end
    clear beaconPreTx beaconPreRSSI beaconPreTime
end

end

