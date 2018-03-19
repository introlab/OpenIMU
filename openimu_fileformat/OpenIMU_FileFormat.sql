
CREATE TABLE tabGroups (
                id_group BIGINT NOT NULL,
                name VARCHAR NOT NULL,
                desc VARCHAR NOT NULL,
                CONSTRAINT tabGroups_pk PRIMARY KEY (id_group)
);


CREATE TABLE tabParticipants (
                id_participant BIGINT NOT NULL,
                id_group BIGINT,
                name VARCHAR NOT NULL,
                desc VARCHAR,
                CONSTRAINT tabParticipants_pk PRIMARY KEY (id_participant),
				FOREIGN KEY (id_group) REFERENCES tabGroups (id_group) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE
);


CREATE TABLE tabRecordsets (
                id_recordset BIGINT NOT NULL,
                id_participant BIGINT NOT NULL,
                name VARCHAR NOT NULL,
                recordset_timestamp TIMESTAMP NOT NULL,
                CONSTRAINT tabRecordsets_pk PRIMARY KEY (id_recordset),
				FOREIGN KEY (id_participant) REFERENCES tabParticipants (id_participant) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE
);


CREATE TABLE tabSubrecords (
                id_subrecord BIGINT NOT NULL,
                id_recordset BIGINT NOT NULL,
                name VARCHAR NOT NULL,
                bout_start_timestamp TIMESTAMP NOT NULL,
                bout_end_timestamp TIMESTAMP NOT NULL,
                CONSTRAINT tabSubrecords_pk PRIMARY KEY (id_subrecord)
				FOREIGN KEY (id_recordset) REFERENCES tabRecordsets (id_recordset) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE
);


CREATE TABLE tabDataProcessors (
                id_data_processor BIGINT NOT NULL,
                name VARCHAR NOT NULL,
                unique_id VARCHAR NOT NULL,
                version FLOAT NOT NULL,
                author VARCHAR NOT NULL,
                custom_script LONGVARCHAR NOT NULL,
                CONSTRAINT tabDataProcessors_pk PRIMARY KEY (id_data_processor)
);


CREATE TABLE tabProcessedData (
                id_processed_data BIGINT NOT NULL,
                tabBouts_id_bout BIGINT NOT NULL,
                id_recordset BIGINT,
                id_data_processor BIGINT NOT NULL,
                id_subrecord BIGINT,
                name VARCHAR NOT NULL,
                data BLOB NOT NULL,
                data_timestamp TIMESTAMP NOT NULL,
                CONSTRAINT tabProcessedData_pk PRIMARY KEY (id_processed_data),
				FOREIGN KEY (id_recordset) REFERENCES tabRecordsets (id_recordset) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE,
				FOREIGN KEY (tabBouts_id_bout) REFERENCES tabSubrecords (id_subrecord) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE,
				FOREIGN KEY (id_data_processor) REFERENCES tabDataProcessors (id_data_processor) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE
);


CREATE TABLE tabDataSet (
                name VARCHAR NOT NULL,
                desc VARCHAR,
                creation_date TIMESTAMP NOT NULL,
                upload_date TIMESTAMP NOT NULL,
                author VARCHAR NOT NULL
);


CREATE TABLE tabDataFormat (
                id_data_format BIGINT NOT NULL,
                name VARCHAR NOT NULL,
                precision INTEGER NOT NULL,
                floating_point BOOLEAN NOT NULL,
                CONSTRAINT tabDataFormat_pk PRIMARY KEY (id_data_format)
);


CREATE TABLE tabSensorsTypes (
                id_sensor_type BIGINT NOT NULL,
                name VARCHAR NOT NULL,
                desc VARCHAR NOT NULL,
                channels INTEGER NOT NULL,
                display_style INTEGER NOT NULL,
                CONSTRAINT tabSensorsTypes_pk PRIMARY KEY (id_sensor_type)
);


CREATE TABLE tabSensors (
                id_sensor BIGINT NOT NULL,
                id_data_format BIGINT NOT NULL,
                id_sensor_type BIGINT NOT NULL,
                name VARCHAR NOT NULL,
                hw_name VARCHAR NOT NULL,
                location VARCHAR NOT NULL,
                sampling_rate INTEGER NOT NULL,
                data_rate INTEGER NOT NULL,
                CONSTRAINT tabSensors_pk PRIMARY KEY (id_sensor),
				FOREIGN KEY (id_data_format) REFERENCES tabDataFormat (id_data_format) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE,
				FOREIGN KEY (id_sensor_type) REFERENCES tabSensorsTypes (id_sensor_type) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE
);


CREATE TABLE tabNotebook (
                id_note BIGINT NOT NULL,
                tabProcessedData_id_processed_data BIGINT,
                id_sensor BIGINT,
                id_processed_data BIGINT,
                id_subrecord BIGINT,
                id_data_processor BIGINT,
                id_recordset BIGINT,
                id_participant BIGINT,
                id_group BIGINT,
                id_data_processed BIGINT,
                note VARCHAR NOT NULL,
                CONSTRAINT tabNotebook_pk PRIMARY KEY (id_note),
				FOREIGN KEY (id_group) REFERENCES tabGroups (id_group) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE,
				FOREIGN KEY (id_participant) REFERENCES tabParticipants (id_participant) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE,
				FOREIGN KEY (id_recordset) REFERENCES tabRecordsets (id_recordset) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE,
				FOREIGN KEY (id_subrecord) REFERENCES tabSubrecords (id_subrecord) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE,
				FOREIGN KEY (id_data_processor) REFERENCES tabDataProcessors (id_data_processor) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE,
				FOREIGN KEY (id_processed_data) REFERENCES tabProcessedData (id_processed_data) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE,
				FOREIGN KEY (tabProcessedData_id_processed_data) REFERENCES tabProcessedData (id_processed_data) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE,
				FOREIGN KEY (id_sensor) REFERENCES tabSensors (id_sensor) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE
);


CREATE TABLE tabCalibration (
                id_calibration BIGINT NOT NULL,
                id_sensor BIGINT NOT NULL,
                data BLOB NOT NULL,
                CONSTRAINT tabCalibration_pk PRIMARY KEY (id_calibration),
				FOREIGN KEY (id_sensor) REFERENCES tabSensors (id_sensor) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE
);


CREATE TABLE tabSensorsData (
                id_sensor_data BIGINT NOT NULL,
                id_recordset BIGINT NOT NULL,
                id_sensor BIGINT NOT NULL,
                data_timestamp TIMESTAMP NOT NULL,
                data BLOB NOT NULL,
                CONSTRAINT tabSensorsData_pk PRIMARY KEY (id_sensor_data)
				FOREIGN KEY (id_recordset) REFERENCES tabRecordsets (id_recordset) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE,
				FOREIGN KEY (id_sensor) REFERENCES tabSensors (id_sensor) ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE
);


CREATE TABLE tabInfos (
                file_version FLOAT NOT NULL
);
