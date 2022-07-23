"""Load precipitation data to database

This module contains functions to load precipitation information to a sqlite database and a zipped json file.

The module exports the following functions:

    _create_connection  Establishes a connection to a sqlite database
    write_to_db         Writes the precipitation data to the sqlite database
    dump_to_json        Writes the precipitation data to a zipped json file
"""

import sqlite3
import pandas as pd


def _create_connection(db_path):
    """Establishes a connection to a sqlite database.

    Parameters
    ----------
    db_path : str
        The path of the sqlite database. If the path does not exist, a new database will be created.

    Returns
    -------
    sqlite3.connection object
        The connection object for the database.

    Raises
    ------
    FileNotFoundError
        If the argument passed is not a valid filepath.
    """

    try:
        connection = sqlite3.connect(db_path)
    except sqlite3.OperationalError:
        raise FileNotFoundError("Database connection could not be made.")
    return connection


def write_to_db(db_path, table_name, data):
    """Writes the precipitation data to a sqlite database.

    This function writes the information in the data parameter to a sqlite database, based on the db_path parameter.
    The data is written to a new table, defined in the table_name parameter. If the table already exists, the data
    is appended to the table.

    Parameters
    ----------
    db_path : str
        The path of the sqlite database. If the path does not exist, a new database will be created.
    table_name : str
        The name of the table to write the data to.
    data : pandas.DataFrame
        A pandas dataframe containing the data to be written to the table.

    Returns
    -------
    boolean
        True if the data is written successfully. Otherwise, False.
    """

    try:
        connection = _create_connection(db_path)
    except FileNotFoundError as exc:
        print(exc)
        return False
    else:
        data.to_sql(table_name, connection, if_exists="append", index=False)
        connection.close()
        return True


def dump_to_json(json_path, data):
    """Writes precipitation data to a zipped json file.

    Parameters
    ----------
    json_path : str
        The path of the json file to be created.
    data : pandas.DataFrame
        A pandas dataframe object containing the data to be written.

    Raises
    ------
    TypeError
        If the data argument passed is not a pandas dataframe.

    Notes
    ----
    The output json file is compressed to avoid potentially large files being written unzipped.
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError("Data input must be a pandas dataframe object.")
    data.to_json(path_or_buf=json_path, orient="records", indent=4, compression="zip")
