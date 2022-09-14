import unittest
from pandas import read_excel
from validator import is_valid, columns_type, check_mandatory
import os


class files(unittest.TestCase):
    def setUp(self):
        configs_path = os.path.join(os.getcwd(), 'tests/resource/Geral_SP.xlsx')
        self.data = read_excel(configs_path, parse_dates=True,  dtype=columns_type())

    # ========================================================================================================== #
    #                                          check of the functions                                            #
    # ========================================================================================================== #
    # def test_check_mandatory(self):
    #     fixture = self.data.copy()

    #     fixture = fixture.rename(columns={'Programas': 'new_program'})
    #     with self.assertRaises(AssertionError) as ctx:
    #         check_mandatory(fixture, 'test_file', columns_type())

    #     self.assemaaartEqual(f"test_file: Expected mandatory arument ['new_program'] in received args: {self.data.key()}.", str(ctx.exception))


    def test_check_mandatory_(self):
        fixture = self.data.copy()

        fixture['RAT'] = fixture['RAT'].astype(int)
        with self.assertRaises(AssertionError) as ctx:
            check_mandatory(fixture, 'test_file', columns_type())

        self.assertEqual(f"test_file: Expected argument ['RAT'] is {float}.", str(ctx.exception))


    def test_functions(self):
        self.assertTrue(is_valid(self.data, 'test_file', columns_type()))