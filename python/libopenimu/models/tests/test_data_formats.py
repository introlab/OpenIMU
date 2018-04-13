"""

    Unit testing for data_formats
    @authors Simon Brière, Dominic Létourneau
    @date 03/04/2018

"""


import unittest
import numpy as np

from libopenimu.models.data_formats import DataFormat


class DataFormatTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_int8_from_bytes(self):
        val = np.int8(-8)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.SINT8)
        self.assertEqual(val, val2)

    def test_uint8_from_bytes(self):
        val = np.uint8(8)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.UINT8)
        self.assertEqual(val, val2)

    def test_int16_from_bytes(self):
        val = np.int16(-16)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.SINT16)
        self.assertEqual(val, val2)

    def test_uint16_from_bytes(self):
        val = np.uint16(16)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.UINT16)
        self.assertEqual(val, val2)

    def test_int32_from_bytes(self):
        val = np.int32(-32)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.SINT32)
        self.assertEqual(val, val2)

    def test_uint32_from_bytes(self):
        val = np.uint32(32)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.UINT32)
        self.assertEqual(val, val2)

    def test_int64_from_bytes(self):
        val = np.int64(-64)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.SINT64)
        self.assertEqual(val, val2)

    def test_uint64_from_bytes(self):
        val = np.uint64(64)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.UINT64)
        self.assertEqual(val, val2)

    def test_float32_from_bytes(self):
        val = np.float32(32.0)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.FLOAT32)
        self.assertEqual(val, val2)

    def test_float64_from_bytes(self):
        val = np.float64(64.0)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.FLOAT64)
        self.assertEqual(val, val2)
