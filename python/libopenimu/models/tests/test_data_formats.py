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

    def test_validation(self):
        self.assertTrue(DataFormat.is_valid(DataFormat.UINT8), 'UINT8 invalid')
        self.assertTrue(DataFormat.is_valid(DataFormat.SINT8), 'SINT8 invalid')
        self.assertTrue(DataFormat.is_valid(DataFormat.UINT16), 'UINT16 invalid')
        self.assertTrue(DataFormat.is_valid(DataFormat.SINT16), 'SINT16 invalid')
        self.assertTrue(DataFormat.is_valid(DataFormat.UINT32), 'UINT32 invalid')
        self.assertTrue(DataFormat.is_valid(DataFormat.SINT32), 'SINT32 invalid')
        self.assertTrue(DataFormat.is_valid(DataFormat.UINT64), 'UINT64 invalid')
        self.assertTrue(DataFormat.is_valid(DataFormat.SINT64), 'SINT64 invalid')
        self.assertTrue(DataFormat.is_valid(DataFormat.FLOAT32), 'FLOAT32 invalid')
        self.assertTrue(DataFormat.is_valid(DataFormat.FLOAT64), 'FLOAT32 invalid')

    def test_int8_from_bytes(self):
        val = np.int8(-8)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.SINT8)
        self.assertEqual(val, val2)

        # Array
        val3 = np.zeros(40, dtype=np.int8)
        val4 = DataFormat.from_bytes(val3.tobytes(), DataFormat.SINT8)
        self.assertTrue((val3 == val4).all())

    def test_uint8_from_bytes(self):
        val = np.uint8(8)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.UINT8)
        self.assertEqual(val, val2)

        # Array
        val3 = np.zeros(40, dtype=np.uint8)
        val4 = DataFormat.from_bytes(val3.tobytes(), DataFormat.UINT8)
        self.assertTrue((val3 == val4).all())

    def test_int16_from_bytes(self):
        val = np.int16(-16)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.SINT16)
        self.assertEqual(val, val2)

        # Array
        val3 = np.zeros(40, dtype=np.int16)
        val4 = DataFormat.from_bytes(val3.tobytes(), DataFormat.SINT16)
        self.assertTrue((val3 == val4).all())

    def test_uint16_from_bytes(self):
        val = np.uint16(16)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.UINT16)
        self.assertEqual(val, val2)

        # Array
        val3 = np.zeros(40, dtype=np.uint16)
        val4 = DataFormat.from_bytes(val3.tobytes(), DataFormat.UINT16)
        self.assertTrue((val3 == val4).all())

    def test_int32_from_bytes(self):
        val = np.int32(-32)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.SINT32)
        self.assertEqual(val, val2)

        # Array
        val3 = np.zeros(40, dtype=np.int32)
        val4 = DataFormat.from_bytes(val3.tobytes(), DataFormat.SINT32)
        self.assertTrue((val3 == val4).all())

    def test_uint32_from_bytes(self):
        val = np.uint32(32)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.UINT32)
        self.assertEqual(val, val2)

        # Array
        val3 = np.zeros(40, dtype=np.uint32)
        val4 = DataFormat.from_bytes(val3.tobytes(), DataFormat.UINT32)
        self.assertTrue((val3 == val4).all())

    def test_int64_from_bytes(self):
        val = np.int64(-64)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.SINT64)
        self.assertEqual(val, val2)

        # Array
        val3 = np.zeros(40, dtype=np.int64)
        val4 = DataFormat.from_bytes(val3.tobytes(), DataFormat.SINT64)
        self.assertTrue((val3 == val4).all())

    def test_uint64_from_bytes(self):
        val = np.uint64(64)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.UINT64)
        self.assertEqual(val, val2)

        # Array
        val3 = np.zeros(40, dtype=np.uint64)
        val4 = DataFormat.from_bytes(val3.tobytes(), DataFormat.UINT64)
        self.assertTrue((val3 == val4).all())

    def test_float32_from_bytes(self):
        val = np.float32(32.0)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.FLOAT32)
        self.assertEqual(val, val2)

        # Array
        val3 = np.zeros(40, dtype=np.float32)
        val4 = DataFormat.from_bytes(val3.tobytes(), DataFormat.FLOAT32)
        self.assertTrue((val3 == val4).all())

    def test_float64_from_bytes(self):
        val = np.float64(64.0)
        buffer = val.tobytes()
        val2 = DataFormat.from_bytes(buffer, DataFormat.FLOAT64)
        self.assertEqual(val, val2)

        # Array
        val3 = np.zeros(40, dtype=np.float64)
        val4 = DataFormat.from_bytes(val3.tobytes(), DataFormat.FLOAT64)
        self.assertTrue((val3 == val4).all())
