import csv
import os
from precip.precip.string_parse import get_year_range, get_missing_data_value, get_grid_ref_values, \
    get_data_values
from precip.precip.utils import calculate_number_of_years

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TEST_FILE = os.path.join(ROOT_PATH, "resources", "cru-ts-2-10.1991-2000-cutdown.pre")
TEST_OUTPUT = os.path.join(ROOT_PATH, "resources", "test_output.csv")


def extract_data(filepath):
    values_to_write = []
    with open(filepath, "r") as f:
        for line in f:
            if "years" in line.lower():
                start_date, end_date = get_year_range(line)
                date_range = calculate_number_of_years(start_date, end_date)

            if "missing" in line.lower():
                missing_value = get_missing_data_value(line)

            if line.startswith("Grid-ref"):
                x, y = get_grid_ref_values(line)
                for i in range(10):
                    current_line = f.readline()
                    data_values = get_data_values(current_line, missing_value)
                    for value in data_values:
                        new_record = {
                            "Xref": x,
                            "Yref": y,
                            "Date": None,
                            "Value": value
                        }
                        values_to_write.append(new_record)
    # writer.writerows(values_to_write)

    return values_to_write


if __name__ == "__main__":
    values_to_write = extract_data(TEST_FILE)
    with open(TEST_OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Xref", "Yref", "Date", "Value"])
        writer.writeheader()
        writer.writerows(values_to_write[:121])
