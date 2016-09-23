import unittest
from  Tracker import activity_tracker as AT

class MyTestCase(unittest.TestCase):
    def test_something(self):
        a = [1,2,3,4,5,6,7]
        act = AT.Activity_Tracker()
        act.loadInput(a)
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
