import unittest
from datetime import datetime
from precip.precip.string_parse import get_year_range, get_missing_data_value, \
    get_grid_ref_values


class TestGetYearRange(unittest.TestCase):
    def test_get_year_range_valid(self):
        test_line = "[Boxes=   67420] [Years=1991-2000] [Multi=    0.1000] [Missing=-999]"
        start_date, end_date = get_year_range(test_line)
        expected_start_date = datetime(1991, 1, 1)
        expected_end_date = datetime(2000, 12, 1)
        self.assertEqual(expected_start_date, start_date)
        self.assertEqual(expected_end_date, end_date)

    def test_get_year_range_invalid_no_years_flag(self):
        test_line = "test string"
        with self.assertRaises(ValueError):
            get_year_range(test_line)

    def test_get_year_range_boundary_all_lower_case(self):
        test_line = "[Boxes=   67420] [years=1991-2000] [Multi=    0.1000] [Missing=-999]"
        start_date, end_date = get_year_range(test_line)
        expected_start_date = datetime(1991, 1, 1)
        expected_end_date = datetime(2000, 12, 1)
        self.assertEqual(expected_start_date, start_date)
        self.assertEqual(expected_end_date, end_date)


class TestGetMissingDataValue(unittest.TestCase):

    def test_get_missing_data_value_valid(self):
        test_line = "[Boxes=   67420] [Years=1991-2000] [Multi=    0.1000] [Missing=-999]"
        self.assertEqual(-999, get_missing_data_value(test_line))

    def test_get_missing_data_value_invalid_no_missing_flag(self):
        test_line = "test string"
        with self.assertRaises(ValueError):
            get_missing_data_value(test_line)

    def test_get_missing_data_value_boundary_lower_case(self):
        test_line = "[Boxes=   67420] [Years=1991-2000] [Multi=    0.1000] [missing=-999]"
        self.assertEqual(-999, get_missing_data_value(test_line))


class TestGetGridRefValues(unittest.TestCase):

    def test_get_grid_ref_values_valid(self):
        test_line = "Grid-ref=   1, 148"
        x, y = get_grid_ref_values(test_line)
        self.assertEqual(1, x)
        self.assertEqual(148, y)

    def test_get_grid_ref_values_invalid_no_values_present(self):
        test_line = "Grid-ref=           "
        with self.assertRaises(ValueError):
            get_grid_ref_values(test_line)


if __name__ == '__main__':
    unittest.main()
