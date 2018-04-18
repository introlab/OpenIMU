"""

    Unit testing for actigraph
    @authors Dominic Létourneau
    @date 18/04/2018

"""


import unittest
from libopenimu.importers.ActigraphImporter import ActigraphImporter

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
        importer = ActigraphImporter()
        importer.load('../../../resources/samples/test.gt3x')

    def test_async_loading(self):
        importer = ActigraphImporter()

        print('Starting threads...')
        # Start threads
        threads = []
        for i in range(0, 2):
            threads.append(importer.async_load('../../../resources/samples/test.gt3x'))

        print('Waiting for threads...')
        # Wait for threads
        for t in threads:
            t.join()

