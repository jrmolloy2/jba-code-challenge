"""Script to run the precip package

This script executes all logic for the precip package. The package's purpose is to extract information
from a file containing precipitation (rainfall) data and transform and load it into a sqlite database
and a zipped json object.
"""

import os
from precip.etl.transform import transform_data, convert_to_df
from precip.etl.load_to_db import write_to_db, dump_to_json


def run():
    """Executes the precip package."""

    # Get the filepath information from the user
    filepath = input("Enter the filepath of the precipitation file: ")
    output_path = input("Enter the folder to save the outputs to: ")

    # Create the output filepaths where the data will be written to
    sql_path = os.path.join(output_path, "precip.db")
    json_path = os.path.join(output_path, "precip.zip")

    # Extract and transform the data
    data = transform_data(filepath)
    if not data:
        print("No data to write.")
        return

    try:
        df = convert_to_df(data)
    except TypeError as exc:
        print(exc)
        return

    # Load the data to db and json
    dump_to_json(json_path, df)
    success = write_to_db(sql_path, "precip_values", df)

    if success:
        print("Data written to {} successfully.".format(output_path))
    else:
        print("Data could not be written to the database.")


if __name__ == "__main__":
    run()
