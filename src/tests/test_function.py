import unittest
from function import *


class dataflow_mysql(unittest.TestCase):
    def test_hours_to_minutes(self):
        result = round(hours_to_minutes('01:01:00'), 6)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 2.541667)

        with self.assertRaises(AssertionError) as ctx:
            hours_to_minutes(11111)

        self.assertEqual(f"Expected argument ['hour'] is {str}.", str(ctx.exception))


    def test_rounding(self):
        self.assertIsInstance(rounding(1.49), int)
        result = rounding(1.49)
        self.assertEqual(1, result)

        with self.assertRaises(AssertionError) as ctx:
            rounding('error')

        self.assertEqual(f"Expected argument ['number'] is {float}.", str(ctx.exception))


    def test_columns_list(self):
        self.assertIsInstance(columns_list(), list)
