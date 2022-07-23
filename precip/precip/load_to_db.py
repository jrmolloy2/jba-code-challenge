import sqlite3
import pandas as pd


def _create_connection(db_path):
    try:
        connection = sqlite3.connect(db_path)
    except sqlite3.OperationalError:
        raise FileNotFoundError("Database connection could not be made.")
    return connection


def write_to_db(db_path, table_name, data):
    try:
        connection = _create_connection(db_path)
    except FileNotFoundError as exc:
        print(exc)
        return False
    else:
        data.to_sql("precip_values", connection, if_exists="append", index=False)
        connection.close()
        return True


def dump_to_json(json_path, data):
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Data input must be a pandas dataframe object.")
    data.to_json(path_or_buf=json_path, orient="records", indent=4, compression="zip")
