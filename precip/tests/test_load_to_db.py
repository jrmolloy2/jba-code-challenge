import unittest
import os
import pandas as pd
from datetime import datetime
from precip.precip.load_to_db import _create_connection, write_to_db, dump_to_json
from precip.config import RESOURCES

MOCK_DB = os.path.join(RESOURCES, "temp.db")
MOCK_JSON = os.path.join(RESOURCES, "temp.zip")


class TestCreateConnection(unittest.TestCase):
    def test__create_connection_valid(self):
        connection = _create_connection(MOCK_DB)
        self.assertTrue(connection)
        connection.close()

    def test__create_connection_invalid_not_valid_path(self):
        with self.assertRaises(FileNotFoundError):
            _create_connection("ZZ:\\test")


class TestWriteToDb(unittest.TestCase):

    def test_write_to_db_valid(self):
        mock_data = [
            {
                "Xref": 1,
                "Yref": 1,
                "Date": datetime(2022, 1, 1),
                "Value": 320
            },
            {
                "Xref": 2,
                "Yref": 2,
                "Date": datetime(2022, 2, 1),
                "Value": 493
            }
        ]
        df = pd.DataFrame(data=mock_data, columns=list(mock_data[0].keys()))

        result = write_to_db(MOCK_DB, "test", df)

        self.assertTrue(result)

        os.remove(MOCK_DB)

    def test_write_to_db_invalid_cannot_read_db(self):
        self.assertFalse(write_to_db("ZZ:\\test", "test", []))


class TestDumpToJSON(unittest.TestCase):

    def test_dump_to_json_valid(self):
        mock_data = [
            {
                "Xref": 1,
                "Yref": 1,
                "Date": datetime(2022, 1, 1),
                "Value": 320
            },
            {
                "Xref": 2,
                "Yref": 2,
                "Date": datetime(2022, 2, 1),
                "Value": 493
            }
        ]
        df = pd.DataFrame(data=mock_data, columns=list(mock_data[0].keys()))
        dump_to_json(MOCK_JSON, df)
        self.assertTrue(os.path.exists(MOCK_JSON))

        os.remove(MOCK_JSON)

    def test_dump_to_json_invalid_not_df_input(self):
        mock_data = [
            {
                "Xref": 1,
                "Yref": 1,
                "Date": datetime(2022, 1, 1),
                "Value": 320
            },
            {
                "Xref": 2,
                "Yref": 2,
                "Date": datetime(2022, 2, 1),
                "Value": 493
            }
        ]
        with self.assertRaises(TypeError):
            dump_to_json(MOCK_JSON, mock_data)


if __name__ == '__main__':
    unittest.main()
