"""
Base class for every data importer
@authors Dominic Létourneau, Simon Brière
@date 18/04/2018
"""

import threading
import datetime
from typing import Protocol, List, Any
from libopenimu.tools.timing import timing
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Participant import Participant


class ImporterObserver(Protocol):
    """
    Protocol for objects that want to observe importer events
    """

    def on_import_error(self, importer: "BaseImporter", error_message: str) -> None:
        """
        Called when an import error occurs

        Args:
            importer: The importer that generated the error
            error_message: Description of the error
        """
        ...

    def on_import_progress(self, importer: "BaseImporter", progress: float) -> None:
        """
        Called when import progress is updated

        Args:
            importer: The importer reporting progress
            progress: Progress value between 0.0 and 1.0
        """
        ...

    def on_import_started(self, importer: "BaseImporter", filename: str) -> None:
        """
        Called when import process starts

        Args:
            importer: The importer that started
            filename: The file being imported
        """
        ...

    def on_import_completed(self, importer: "BaseImporter", result: Any) -> None:
        """
        Called when import process completes successfully

        Args:
            importer: The importer that completed
            result: The import result
        """
        ...


@timing
def load_worker(importer, filename):
    print("load_worker starting")
    result = importer.load(filename)
    importer.loaded_callback(result)
    print("load worker done")


class BaseImporter:
    last_error = ""

    def __init__(self, manager: DBManager, participant: Participant):

        # This is the manager that will be used for importation, externally created
        self.db = manager

        # This is the participant
        self.participant = participant

        # No recordsets when starting
        self.recordsets = []

        # Observer management
        self._observers: List[ImporterObserver] = []
        self._observer_lock = threading.RLock()

    def add_observer(self, observer: ImporterObserver) -> None:
        """
        Register an observer to receive import events

        Args:
            observer: Object implementing ImporterObserver protocol
        """
        with self._observer_lock:
            if observer not in self._observers:
                self._observers.append(observer)

    def remove_observer(self, observer: ImporterObserver) -> None:
        """
        Unregister an observer

        Args:
            observer: Observer to remove
        """
        with self._observer_lock:
            if observer in self._observers:
                self._observers.remove(observer)

    def clear_observers(self) -> None:
        """
        Remove all registered observers
        """
        with self._observer_lock:
            self._observers.clear()

    def _notify_observers(self, notification_method: str, *args, **kwargs) -> None:
        """
        Notify all registered observers of an event

        Args:
            notification_method: Name of the method to call on observers
            *args: Positional arguments to pass to observer methods
            **kwargs: Keyword arguments to pass to observer methods
        """
        with self._observer_lock:
            observers_copy = self._observers.copy()

        for observer in observers_copy:
            try:
                method = getattr(observer, notification_method, None)
                if method and callable(method):
                    method(*args, **kwargs)
            except Exception as e:
                print(f"Error notifying observer {observer}: {e}")

    def notify_error(self, message: str) -> None:
        """
        Notify observers of an import error
        """
        self.last_error = message
        print("Error in importer: " + message)
        self._notify_observers("on_import_error", self, message)

    def notify_progress(self, progress: float) -> None:
        """
        Notify observers of import progress
        """
        print("Progress: " + str(progress))
        self._notify_observers("on_import_progress", self, progress)

    def notify_import_started(self, filename: str) -> None:
        """
        Notify observers that import has started
        """
        print("Import started: " + filename)
        self._notify_observers("on_import_started", self, filename)

    def notify_import_completed(self, result: Any) -> None:
        """
        Notify observers that import has completed
        """
        print("Import completed")
        self._notify_observers("on_import_completed", self, result)

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
        recordset = self.db.add_recordset(
            self.participant, session_name, my_time, my_time
        )
        self.recordsets.append(recordset)
        return recordset

    def clear_recordsets(self):
        self.recordsets = []

    def async_load(self, filename):
        print("will call load on importer with filename: ", filename)
        self.notify_import_started(filename)
        t = threading.Thread(target=load_worker, args=[self, filename])
        t.start()
        return t

    def load(self, filename):
        print("Nothing to do in " + type(self) + ".load")

    def import_to_database(self, results):
        print("Nothing to do in " + type(self) + " import to database.")

    def loaded_callback(self, result):
        print("loaded callback result len", len(result))
        self.notify_import_completed(result)
        self.import_to_database(result)

    def add_recordset_to_db(self, name, start_timestamp, stop_timestamp):
        recordset = self.db.add_recordset(
            self.participant, name, start_timestamp, stop_timestamp
        )
        return recordset

    def add_sensor_to_db(
        self,
        sensor_type,
        name,
        hw_name,
        location,
        sampling_rate,
        data_rate,
        settings: str | None = None,
        hw_id: str | None = None,
    ):
        sensor = self.db.add_sensor(
            sensor_type,
            name,
            hw_name,
            location,
            sampling_rate,
            data_rate,
            settings,
            hw_id,
        )
        return sensor

    def add_channel_to_db(self, sensor, unit, data_format, label):
        channel = self.db.add_channel(sensor, unit, data_format, label)
        return channel

    def add_sensor_data_to_db(self, recordset, sensor, channel, timestamps, data):
        sensor_data = self.db.add_sensor_data(
            recordset, sensor, channel, timestamps, data
        )
        return sensor_data

    def add_datasource_to_db(self, filename, file_start_time):
        pass
