import re
from datetime import datetime


def remove_whitespace(line):
    if not isinstance(line, str):
        raise TypeError("The argument passed must be a string.")
    return re.sub("\s", "", line)


def calculate_number_of_years(start_date, end_date):
    if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
        raise TypeError("Dates passed must be datetime objects.")
    return (end_date.year - start_date.year) + 1
