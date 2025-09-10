"""

Unit testing for actigraph
@authors Dominic Létourneau
@date 18/04/2018

"""

import unittest
import os
import libopenimu.importers.actigraph as actigraph
import numpy as np


class ActigraphTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_loading(self):

        np.set_printoptions(suppress=True)
        print("Testing gt3x importer")

        # Epoch separated data
        # Get path of current file without file name
        dirname = os.path.dirname(__file__)
        [info, my_dict] = actigraph.gt3x_importer(
            os.path.join(dirname, "samples/test.gt3x")
        )

        self.assertTrue(len(info) > 0)
        self.assertTrue(len(my_dict) > 0)
