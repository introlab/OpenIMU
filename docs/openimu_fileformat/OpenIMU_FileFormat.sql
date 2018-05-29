
CREATE TABLE tabUnits (
                id_unit INTEGER PRIMARY KEY NOT NULL,
                name VARCHAR NOT NULL
);


CREATE TABLE tabSensorTypes (
                id_sensor_type INTEGER PRIMARY KEY NOT NULL,
                name VARCHAR NOT NULL
);


CREATE TABLE tabGroups (
                id_group INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name VARCHAR NOT NULL,
                description VARCHAR NOT NULL);


CREATE TABLE tabParticipants (
                id_participant INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_group INTEGER,
                name VARCHAR NOT NULL,
                description VARCHAR,
		FOREIGN KEY (id_group) REFERENCES tabGroups (id_group) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabRecordsets (
                id_recordset INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_participant INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                start_timestamp DATETIME NOT NULL,
                end_timestamp DATETIME NOT NULL,
		FOREIGN KEY (id_participant) REFERENCES tabParticipants (id_participant) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabSubrecords (
                id_subrecord INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_recordset INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                start_timestamp DATETIME NOT NULL,
                end_timestamp DATETIME NOT NULL,
		FOREIGN KEY (id_recordset) REFERENCES tabRecordsets (id_recordset) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabDataProcessors (
                id_data_processor INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name VARCHAR NOT NULL,
                unique_id VARCHAR NOT NULL,
                version DOUBLE PRECISIONS NOT NULL,
                author VARCHAR NOT NULL,
                custom_script TEXT NOT NULL
);


CREATE TABLE tabDataSet (
                name VARCHAR NOT NULL,
                description VARCHAR,
                creation_date DATETIME NOT NULL,
                upload_date DATETIME NOT NULL,
                author VARCHAR NOT NULL
);


CREATE TABLE tabDataFormat (
                id_data_format INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                PRIMARY KEY (id_data_format)
);


CREATE TABLE tabSensors (
                id_sensor INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_sensor_type INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                hw_name VARCHAR NOT NULL,
                location VARCHAR NOT NULL,
                sampling_rate FLOAT NOT NULL,
                data_rate INTEGER NOT NULL,
		FOREIGN KEY (id_sensor_type) REFERENCES tabSensorTypes (id_sensor_type) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabChannels (
                id_channel INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_sensor INTEGER NOT NULL,
                id_unit INTEGER NOT NULL,
                id_data_format BIGINTEGER NOT NULL,
                label VARCHAR NOT NULL,
		FOREIGN KEY (id_unit) REFERENCES tabUnits (id_unit) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_data_format) REFERENCES tabDataFormat (id_data_format) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_sensor) REFERENCES tabSensors (id_sensor) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabProcessedData (
                id_processed_data INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_subrecord INTEGER NOT NULL,
                id_recordset INTEGER NOT NULL,
                id_channel INTEGER,
                id_data_processor INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                data LONGBLOB NOT NULL,
                data_timestamp DATETIME NOT NULL,
		FOREIGN KEY (id_recordset) REFERENCES tabRecordsets (id_recordset) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_subrecord) REFERENCES tabSubrecords (id_subrecord) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_data_processor) REFERENCES tabDataProcessors (id_data_processor) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_channel) REFERENCES tabChannels (id_channel) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabNotebook (
                id_note INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_sensor INTEGER NOT NULL,
                id_processed_data INTEGER NOT NULL,
                id_subrecord INTEGER NOT NULL,
                id_data_processor INTEGER NOT NULL,
                id_recordset INTEGER NOT NULL,
                id_participant INTEGER NOT NULL,
                id_group INTEGER NOT NULL,
                note VARCHAR NOT NULL,
		FOREIGN KEY (id_group) REFERENCES tabGroups (id_group) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_participant) REFERENCES tabParticipants (id_participant) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_recordset) REFERENCES tabRecordsets (id_recordset) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_subrecord) REFERENCES tabSubrecords (id_subrecord) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_data_processor) REFERENCES tabDataProcessors (id_data_processor) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_sensor) REFERENCES tabSensors (id_sensor) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_processed_data) REFERENCES tabProcessedData (id_processed_data) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabCalibration (
                id_calibration INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_sensor INTEGER NOT NULL,
                data LONGBLOB NOT NULL,
		FOREIGN KEY (id_sensor) REFERENCES tabSensors (id_sensor) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabSensorsData (
                id_sensor_data INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_recordset INTEGER NOT NULL,
                id_sensor INTEGER NOT NULL,
                id_channel INTEGER NOT NULL,
                data_timestamp DATETIME NOT NULL,
                data LONGBLOB NOT NULL,
		FOREIGN KEY (id_recordset) REFERENCES tabRecordsets (id_recordset) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_sensor) REFERENCES tabSensors (id_sensor) ON DELETE CASCADE ON UPDATE NO ACTION,
		FOREIGN KEY (id_channel) REFERENCES tabChannels (id_channel) ON DELETE CASCADE ON UPDATE NO ACTION
);


CREATE TABLE tabInfos (
                file_version DOUBLE PRECISIONS NOT NULL
);
