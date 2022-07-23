import re


def remove_whitespace(line):
    if not isinstance(line, str):
        raise TypeError("The argument passed must be a string.")
    return re.sub("\s", "", line)


def calculate_number_of_years(start_date, end_date):
    if isinstance(start_date, int) and isinstance(end_date, int):
        return (end_date - start_date) + 1
    else:
        raise TypeError("Dates passed must be integers.")


def get_year_range(line):
    pattern = re.compile("(?i)Years=\d{4}-\d{4}")
    match = pattern.search(line)
    if match:
        dates = match.group()[6:].split("-")
        start_date = int(dates[0])
        end_date = int(dates[1])
        return start_date, end_date
    else:
        raise ValueError("The date range for the file could not be found.")


def get_missing_data_value(line):
    # TODO handle non negative values
    pattern = re.compile("(?i)Missing=.\d+")
    match = pattern.search(line)
    if match:
        return int(match.group()[8:])
    else:
        print("Missing data value could not be found. Assume value to be -999.")
        return -999


def get_grid_ref_values(line):
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
    try:
        values = [int(x) for x in line.split()]
    except ValueError:
        raise ValueError("Data values could not be parsed.")
    else:
        for ix, value in enumerate(values):
            if value == missing_value:
                values[ix] = None
        return values
