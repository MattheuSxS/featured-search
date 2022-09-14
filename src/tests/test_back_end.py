import unittest
from back_end import *
from function import columns_type
from pandas import DataFrame, read_excel
import os


class dataflow_mysql(unittest.TestCase):
    def setUp(self):
        configs_path = os.path.join(os.getcwd(), 'tests/file_test/Geral_RJ.xlsx')
        self.data = read_excel(configs_path, parse_dates=True,  dtype=columns_type())


    def test_rat_x_duration(self):
        with self.assertRaises(AssertionError) as ctx:
            rat_x_duration('00:60:00', 1.99999)

        self.assertEqual(f"time data 00:60:00 does not match format %H:%M:%S.", str(ctx.exception))

        with self.assertRaises(AssertionError) as ctx:
            rat_x_duration('01:00:00', int)

        self.assertEqual(f'Expected argument {int} is {float}.', str(ctx.exception))

        self.assertEqual(round(rat_x_duration('01:00:00', 10.666666), 6), 26.666665)


    def test_time_conversion(self):
        with self.assertRaises(AssertionError) as ctx:
            time_conversion('00:60:00')

        self.assertEqual(f"time data 00:60:00 does not match format %H:%M:%S.", str(ctx.exception))

        with self.assertRaises(AssertionError) as ctx:
            rat_x_duration('00:01:00', int)

        self.assertEqual(f"Expected argument {int} is {float}.", str(ctx.exception))

        self.assertEqual(time_conversion('01:00:00'), '01:00')


    # TODO
    # def test_read_file(self):
        # fixture = read_file(self.data)

        # self.assertEqual(type(fixture), DataFrame)

        # with self.assertRaises(AssertionError) as ctx:
        #     read_file(list())

        # self.assertEqual(f"Expected argument ['data'] is {DataFrame}.", str(ctx.exception))


    def test_file_path(self):
        fixture = file_path('SP', 'roject_datalake/gitlab/featured-search/src')

        self.assertIsInstance(fixture, str)

        date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.assertEqual(fixture, f'roject_datalake/gitlab/featured-search/src/CGCOM_{date}_SP.xlsx')


    # #TODO
    # def test_rat_shr_result(self):
    #     fixture = read_file(self.data)

    #     with self.assertRaises(AssertionError) as ctx:
    #         rat_shr_result(list(), 'rat', fixture)

    #     self.assertEqual(f"Expected argument ['day'] is {int}.", str(ctx.exception))

    #     with self.assertRaises(AssertionError) as ctx:
    #         rat_shr_result(1, list(), fixture)

    #     self.assertEqual(f"Expected argument ['option'] is {str}.", str(ctx.exception))

        # self.assertEqual(type(rat_shr_result(1, 'rat', fixture)), DataFrame)
