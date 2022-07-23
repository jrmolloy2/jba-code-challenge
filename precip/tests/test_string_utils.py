import unittest
from precip.precip.string_utils import remove_whitespace


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


if __name__ == '__main__':
    unittest.main()
