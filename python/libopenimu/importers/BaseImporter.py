
"""
    Base class for every data importer
    @authors Dominic Létourneau
    @date 18/04/2018

"""

import threading
from libopenimu.tools.timing import timing
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Participant import Participant

import datetime

from PySide6.QtCore import QObject, Signal


@timing
def load_worker(importer, filename):
    print('load_worker starting')
    result = importer.load(filename)
    importer.loaded_callback(result)
    print('load worker done')


class BaseImporter(QObject):

    update_progress = Signal(int)
    last_error = ""

    def __init__(self, manager: DBManager, participant: Participant, parent=None):
        super(BaseImporter, self).__init__(parent)

        # This is the manager that will be used for importation, externally created
        self.db = manager

        # This is the participant
        self.participant = participant

        # No recordsets when starting
        self.recordsets = []

    def get_recordset(self, timestamp, session_name=str()):
        try:
            my_time = datetime.datetime.fromtimestamp(timestamp)
        except ValueError:
            return None

        # Validate timestamp
        if my_time > datetime.datetime.now() or my_time < datetime.datetime(2000, 1, 1):
            print("Invalid timestamp: " + str(timestamp))
            return None

        # Find a record the same day
        for record in self.recordsets:
            # Same date return this record
            if record.start_timestamp.date() == my_time.date():
                return record

        # Return new record
        recordset = self.db.add_recordset(self.participant, session_name, my_time, my_time)
        self.recordsets.append(recordset)
        return recordset

    def clear_recordsets(self):
        self.recordsets = []

    def async_load(self, filename):
        print('will call load on importer with filename: ', filename)
        t = threading.Thread(target=load_worker, args=[self, filename])
        t.start()
        return t

    def load(self, filename):
        print('Nothing to do in ' + type(self) + ".load")

    def import_to_database(self, results):
        print('Nothing to do in ' + type(self) + " import to database.")

    def loaded_callback(self, result):
        print('loaded callback result len', len(result))
        self.import_to_database(result)

    def add_recordset_to_db(self, name, start_timestamp, stop_timestamp):
        recordset = self.db.add_recordset(self.participant, name, start_timestamp, stop_timestamp)
        return recordset

    def add_sensor_to_db(self, sensor_type, name, hw_name, location, sampling_rate, data_rate,
                         settings: str | None = None):
        sensor = self.db.add_sensor(sensor_type, name, hw_name, location, sampling_rate, data_rate, settings)
        return sensor

    def add_channel_to_db(self, sensor, unit, data_format, label):
        channel = self.db.add_channel(sensor, unit, data_format, label)
        return channel

    def add_sensor_data_to_db(self, recordset, sensor, channel, timestamps, data):
        sensor_data = self.db.add_sensor_data(recordset, sensor, channel, timestamps, data)
        return sensor_data

    def add_datasource_to_db(self, filename, file_start_time):
        pass
