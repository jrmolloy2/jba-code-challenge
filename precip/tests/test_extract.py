import unittest
from precip.etl.extract import remove_whitespace, calculate_number_of_years, get_year_range, get_missing_data_value, \
    get_grid_ref_values, get_data_values


class TestRemoveWhitespace(unittest.TestCase):

    def test_remove_whitespace_valid(self):
        test_line = "Grid-ref=      1,    148        "
        self.assertEqual("Grid-ref=1,148", remove_whitespace(test_line))

    def test_remove_whitespace_invalid_string_not_passed(self):
        with self.assertRaises(TypeError):
            remove_whitespace(123)

    def test_remove_whitespace_boundary_includes_escaped_newline_character(self):
        test_line = "Grid-ref=        1,    148\n"
        self.assertEqual("Grid-ref=1,148", remove_whitespace(test_line))


class TestCalculateNumberOfYears(unittest.TestCase):

    def test_calculate_number_of_years_valid(self):
        self.assertEqual(10, calculate_number_of_years(2001, 2010))

    def test_calculate_number_of_years_invalid_not_integers(self):
        with self.assertRaises(TypeError):
            calculate_number_of_years("2001", "2010")


class TestGetYearRange(unittest.TestCase):
    def test_get_year_range_valid(self):
        test_line = "[Boxes=   67420] [Years=1991-2000] [Multi=    0.1000] [Missing=-999]"
        start_date, end_date = get_year_range(test_line)
        self.assertEqual(1991, start_date)
        self.assertEqual(2000, end_date)

    def test_get_year_range_invalid_no_years_flag(self):
        test_line = "test string"
        with self.assertRaises(ValueError):
            get_year_range(test_line)

    def test_get_year_range_boundary_all_lower_case(self):
        test_line = "[Boxes=   67420] [years=1991-2000] [Multi=    0.1000] [Missing=-999]"
        start_date, end_date = get_year_range(test_line)
        self.assertEqual(1991, start_date)
        self.assertEqual(2000, end_date)


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


class TestGetDataValues(unittest.TestCase):

    def test_get_data_values_valid(self):
        test_line = " 3020 2820 3040 2880 1740 1360  980  990 1410 1770 2580 2630"
        expected = [3020, 2820, 3040, 2880, 1740, 1360, 980, 990, 1410, 1770, 2580, 2630]
        self.assertEqual(expected, get_data_values(test_line, -999))

    def test_get_data_values_valid_with_missing_value(self):
        test_line = "  -999  2010 193 4576"
        self.assertEqual([None, 2010, 193, 4576], get_data_values(test_line, -999))

    def test_get_data_values_invalid_not_space_delimited(self):
        test_line = "3020;2820;3040;2880;1740"
        with self.assertRaises(ValueError):
            get_data_values(test_line, -999)


if __name__ == '__main__':
    unittest.main()
