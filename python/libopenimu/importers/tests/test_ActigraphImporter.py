"""

    Unit testing for actigraph
    @authors Dominic Létourneau
    @date 18/04/2018

"""


import unittest
from libopenimu.importers.ActigraphImporter import ActigraphImporter
from libopenimu.db.DBManager import DBManager
from libopenimu.models.sensor_types import SensorType
from libopenimu.models.Participant import Participant

import numpy as np


class ActigraphImporterTest(unittest.TestCase):

    def setUp(self):
        np.set_printoptions(suppress=True)
        print('Testing ActigraphImporter')

    def thread_finished_callback(self):
        pass

    def tearDown(self):
        pass

    def test_loading(self):

        manager = DBManager('test.db', overwrite=True)
        participant = Participant(name='My Participant', description='Participant Description')
        manager.update_participant(participant)

        # Import to database
        importer = ActigraphImporter(manager, participant)
        results = importer.load('../../../resources/samples/test.gt3x')

        samples = 0
        for activity in results[1]['activity']:
            samples += 3 * len(activity[1])

        print('samples imported (each channels)', samples)

        importer.import_to_database(results)


        # Reload from database
        manager = DBManager('test.db')

        recordsets = manager.get_all_recordsets()
        self.assertEqual(len(recordsets), 1)

        loaded_samples = 0

        for record in recordsets:
            # Get all sensors in record
            sensors = manager.get_all_sensors()
            for sensor in sensors:
                if sensor.id_sensor_type == SensorType.ACCELEROMETER:
                    channels = manager.get_all_channels(sensor=sensor)
                    for channel in channels:
                        print('processing channel: ', channel)
                        self.assertEqual(channel.id_sensor, sensor.id_sensor, "id_sensor test for channel")
                        # Will get all data (converted to floats)
                        channel_data = manager.get_all_sensor_data(recordset=record, convert=True,
                                                                   channel=channel)
                        print('channel_data_length', len(channel_data))

                        for sensor_data in channel_data:
                            self.assertEqual(sensor_data.id_channel, channel.id_channel, "id_channel test for data")
                            self.assertEqual(sensor_data.id_sensor, sensor.id_sensor, "id_sensor test data")
                            loaded_samples += len(sensor_data.data)

        self.assertEqual(samples, loaded_samples)

    def test_async_loading(self):

        manager = DBManager('test.db', overwrite=True)
        participant = Participant(name='My Participant', description='Participant Description')
        manager.update_participant(participant)

        importer = ActigraphImporter(manager, participant)

        print('Starting threads...')
        # Start threads
        threads = []
        for i in range(0, 1):
            threads.append(importer.async_load('../../../resources/samples/test.gt3x'))

        print('Waiting for threads...')
        # Wait for threads
        for t in threads:
            t.join()

        recordsets = manager.get_all_recordsets(participant)
        print('recordsets', recordsets)
        self.assertGreater(len(recordsets), 0)


