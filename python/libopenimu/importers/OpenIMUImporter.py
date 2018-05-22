from libopenimu.importers.BaseImporter import BaseImporter




from libopenimu.models.sensor_types import SensorType
from libopenimu.models.units import Units
from libopenimu.models.Recordset import Recordset
from libopenimu.models.data_formats import DataFormat
from libopenimu.tools.timing import timing
from libopenimu.db.DBManager import DBManager
from libopenimu.models.Participant import Participant

import numpy as np
import datetime


class OpenIMUImporter(BaseImporter):
    def __init__(self, manager: DBManager, participant: Participant):
        super().__init__(manager, participant)
        print('OpenIMU Importer')
        # No recordsets when starting
        self.recordsets = []

    def load(self, filename):
        print('OpenIMUImporter.load')
        pass

    def import_to_database(self, result):
        print('OpenIMUImporter.import_to_database')
        pass
