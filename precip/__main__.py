import os
from precip.precip.transform import transform_data, convert_to_df
from precip.precip.load_to_db import write_to_db, dump_to_json


def run():

    filepath = input("Enter the filepath of the precipitation file: ")
    output_path = input("Enter the folder to save the outputs to: ")

    sql_path = os.path.join(output_path, "precip.db")
    json_path = os.path.join(output_path, "precip.zip")

    data = transform_data(filepath)
    if not data:
        print("No data to write.")
        return

    try:
        df = convert_to_df(data)
    except TypeError as exc:
        print(exc)
        return

    dump_to_json(json_path, df)
    success = write_to_db(sql_path, "precip_values", df)

    if success:
        print("Data written to {} successfully.".format(output_path))
    else:
        print("Data could not be written to the database.")


if __name__ == "__main__":
    run()
