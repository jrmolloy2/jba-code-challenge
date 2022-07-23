"""Transform precipitation data to pandas dataframe

This module contains functions to transform precipitation information from a text file to a pandas DataFrame.

The module exports the following functions:

    transform_data  Transforms raw strings from the precipitation file to a json-like list of dictionaries.
    convert_to_df   Converts a json-like list of dictionaries to a pandas DataFrame.
"""

import pandas as pd
import os
from datetime import datetime
from precip.etl.extract import get_year_range, get_missing_data_value, get_grid_ref_values, \
    get_data_values, calculate_number_of_years


def transform_data(filepath):
    """Returns a list of dictionaries containing precipitation data from the text file.

    This function reads the precipitation file passed as an argument and transforms the raw string information
    to a list of dictionaries that can be loaded to a database. This function depends on the extract module
    of the precip package.

    Parameters
    ----------
    filepath : str
        The path of the precipitation file to be transformed.

    Returns
    -------
    values_to_write : list
        A list of dictionaries containing the data from the precipitation file.

    Raises
    ------
    FileNotFoundError
        If the filepath cannot be found.
    """

    # Check the file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError("The precipitation file entered could not be found.")

    values_to_write = []
    with open(filepath, "r") as f:
        for line in f:
            # Get the start and end year if 'years' is in the line
            if "years" in line.lower():
                try:
                    start_date, end_date = get_year_range(line)
                except ValueError as exc:
                    return None

                # Calculate the number of years included in the file (e.g 10)
                date_range = calculate_number_of_years(start_date, end_date)

            # Get the missing data value (assumed to be -999 is missing flag not present)
            if "missing" in line.lower():
                missing_value = get_missing_data_value(line)

            # If the line is a grid-ref line, use this as a marker for the rainfall data
            if line.startswith("Grid-ref"):
                # Get the x and y values first
                try:
                    x, y = get_grid_ref_values(line)
                except ValueError as exc:
                    print(exc)
                    return None
                else:
                    # Loop through the years
                    for i in range(date_range):
                        # Read the next line
                        current_line = f.readline()
                        # Get the values from the line
                        # If no values, there is a problem with the file and the script ends
                        try:
                            data_values = get_data_values(current_line, missing_value)
                        except ValueError as exc:
                            print(exc)
                            return None
                        # Loop through the monthly data in the line and create a record
                        for month, value in enumerate(data_values):
                            new_record = {
                                "Xref": x,
                                "Yref": y,
                                "Date": datetime(start_date + i, month + 1, 1),
                                "Value": value
                            }
                            values_to_write.append(new_record)

    return values_to_write


def convert_to_df(data):
    """Creates a pandas DataFrame from a list of dictionaries.

    Parameters
    ----------
    data : list
        A list of dictionaries containing the data to be converted to dataframe.

    Returns
    -------
    pandas.DataFrame
        The DataFrame containing the final data.

    Raises
    ------
    TypeError
        If the argument passed a list of dictionaries.
    """

    if any(not isinstance(record, dict) for record in data):
        raise TypeError("The data passed must be a list of dictionaries.")
    return pd.DataFrame(data=data, columns=list(data[0].keys()))
