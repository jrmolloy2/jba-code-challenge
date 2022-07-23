import unittest
from datetime import datetime
from precip.precip.transform import transform_data, convert_to_df
from precip.config import TEST_FILE


class TestTransformData(unittest.TestCase):

    def test_transform_data_valid(self):
        output = transform_data(TEST_FILE)
        self.assertIsInstance(output, list)
        self.assertEqual(627115, len(output))

    def test_transform_data_invalid_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            transform_data("C:\\test_path")


class TestConvertToDf(unittest.TestCase):

    def test_convert_to_df_valid(self):
        data = [
            {"Xref": 1,
             "Yref": 148,
             "Date": datetime(2000, 1, 1),
             "Value": 300},
            {"Xref": 1,
             "Yref": 150,
             "Date": datetime(2000, 1, 1),
             "Value": 293}
        ]
        self.assertEqual(2, len(convert_to_df(data)))

    def test_convert_to_df_invalid_not_dict(self):
        data = [1, 2, 3, 4]
        with self.assertRaises(TypeError):
            convert_to_df(data)


if __name__ == '__main__':
    unittest.main()
