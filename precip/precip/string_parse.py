import re
from datetime import datetime
from precip.precip.utils import remove_whitespace


def get_year_range(line):
    pattern = re.compile("(?i)Years=\d{4}-\d{4}")
    match = pattern.search(line)
    if match:
        dates = match.group()[6:].split("-")
        start_date = datetime(int(dates[0]), 1, 1)
        end_date = datetime(int(dates[1]), 12, 1)
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
        raise ValueError("The missing data value could not be parsed.")


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
    except ValueError as exc:
        raise exc
    else:
        for ix, value in enumerate(values):
            if value == missing_value:
                values[ix] = None
        return values
