import pandas as pd
import os
from datetime import datetime
from precip.precip.extract import get_year_range, get_missing_data_value, get_grid_ref_values, \
    get_data_values, calculate_number_of_years


def transform_data(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError("The precipitation file entered could not be found.")

    values_to_write = []
    with open(filepath, "r") as f:
        for line in f:
            if "years" in line.lower():
                try:
                    start_date, end_date = get_year_range(line)
                except ValueError as exc:
                    return None

                date_range = calculate_number_of_years(start_date, end_date)

            if "missing" in line.lower():
                missing_value = get_missing_data_value(line)

            if line.startswith("Grid-ref"):
                try:
                    x, y = get_grid_ref_values(line)
                except ValueError as exc:
                    print(exc)
                    return None
                else:
                    for i in range(date_range):
                        current_line = f.readline()
                        try:
                            data_values = get_data_values(current_line, missing_value)
                        except ValueError as exc:
                            print(exc)
                            return None
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
    if any(not isinstance(record, dict) for record in data):
        raise TypeError("The data passed must be a list of dictionaries.")
    return pd.DataFrame(data=data, columns=list(data[0].keys()))
