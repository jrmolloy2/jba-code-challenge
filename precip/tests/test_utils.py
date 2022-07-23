import unittest
from datetime import datetime
from precip.precip.utils import remove_whitespace, calculate_number_of_years


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
        self.assertEqual(10, calculate_number_of_years(datetime(2001, 1, 1), datetime(2010, 1, 1)))

    def test_calculate_number_of_years_invalid_not_datetime_objects(self):
        with self.assertRaises(TypeError):
            calculate_number_of_years(2001, 2010)


if __name__ == '__main__':
    unittest.main()
