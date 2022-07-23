"""Extract precipitation data

This module contains functions to extract precipitation information from a .pre file.

The module exports the following functions:

    remove_whitespace          Removes all whitespace characters from a line in the file
    calculate_number_of_years  Returns the number of years the file covers
    get_year_range             Gets the start year and end year from the file
    get_missing_data_value     Gets the fill value from the file
    get_grid_ref_values        Gets the X and Y values from a grid-ref line
    get_data_values            Returns a list of rainfall values from a line
"""

import re


def remove_whitespace(line):
    """Removes all whitespace characters from a string.

    Parameters
    ----------
    line : str
        The string containing whitespace characters.

    Returns
    -------
    str
        The string with whitespace characters removed.

    Raises
    ------
    TypeError
        If the argument passed is not a string.
    """

    if not isinstance(line, str):
        raise TypeError("The argument passed must be a string.")
    return re.sub("\s", "", line)


def calculate_number_of_years(start_date, end_date):
    """Returns how many years are between the start and end dates inclusive.

    Parameters
    ----------
    start_date : int
        The starting year.
    end_date : int
        The ending year.

    Returns
    -------
    int
        The number of years including the start and end year.

    Raises
    ------
    TypeError
        If the arguments passed are not integers.
    """

    if isinstance(start_date, int) and isinstance(end_date, int):
        return (end_date - start_date) + 1
    else:
        raise TypeError("Dates passed must be integers.")


def get_year_range(line):
    """Extracts the data from the 'Years=' flag in the precipitation file.

    Parameters
    ----------
    line : str
        The string containing the 'Years=' flag.

    Returns
    -------
    start_date : int
        The first year.
    end_date : int
        The final year.

    Raises
    ------
    ValueError
        If the 'Years=' flag could not be found in the argument.
    """

    # Case insensitive search for 'years=1991-2000' where the years can be any numbers
    pattern = re.compile("(?i)Years=\d{4}-\d{4}")
    match = pattern.search(line)
    if match:
        dates = match.group()[6:].split("-")  # removes unnecessary text
        start_date = int(dates[0])
        end_date = int(dates[1])
        return start_date, end_date
    else:
        raise ValueError("The date range for the file could not be found.")


def get_missing_data_value(line):
    """Extracts the value in the 'Missing=' flag from a precipitation file.

    Parameters
    ----------
    line : str
        The string containing the 'Missing=' flag.

    Returns
    -------
    int
        The missing data value

    Notes
    -----
    If the 'Missing=' flag cannot be found, the missing data value is assumed to be -999.
    """

    # Case insensitive search for 'Missing=-999' where 999 can be any digits
    pattern = re.compile("(?i)Missing=.\d+")
    match = pattern.search(line)
    if match:
        return int(match.group()[8:])
    else:
        print("Missing data value could not be found. Assume value to be -999.")
        return -999


def get_grid_ref_values(line):
    """Extracts X and Y coordinates from a line containing 'Grid-ref='.

    Parameters
    ----------
    line : str
        The string containing the 'Grid-ref=' flag.

    Returns
    -------
    x : int
        The x coordinate found.
    y : int
        The y coordinate found.

    Raises
    ------
    ValueError
        If the grid references could not be found.
    """

    try:
        no_whitespace = remove_whitespace(line)
    except TypeError as exc:
        return None, None
    else:
        pattern = re.compile("\d+,\d+")
        match = pattern.search(no_whitespace)
        if match:
            split_by_comma = match.group().split(",")
            return int(split_by_comma[0]), int(split_by_comma[1])
        else:
            raise ValueError("Grid references could not be parsed.")


def get_data_values(line, missing_value):
    """Extracts the rainfall values from a line in the precipitation file.

    Parameters
    ----------
    line : str
        The string containing rainfall values.
    missing_value : int
        The fill value to be substituted with None.

    Returns
    -------
    list
        A list of integers containing the rainfall data for a line.

    Raises
    ------
    ValueError
        If the line cannot be split into integers.
    """

    try:
        values = [int(x) for x in line.split()]
    except ValueError:
        raise ValueError("Data values could not be parsed.")
    else:
        for ix, value in enumerate(values):
            if value == missing_value:
                values[ix] = None
        return values
