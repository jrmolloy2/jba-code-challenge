# JBA Code Challenge - Precipitation Data

## Project description

This package is a submission to [JBA Software's code challenge](https://jbasoftware.com/careers/code-challenge/). The purpose of the package is to read precipitation (rainfall) data from a text file and to transform that data
into a database with the following structure:

| Xref | Yref | Date | Value |
|------|------|------|-------|
| 1 | 311 | 01/01/1991 | 320 |

I made the following assumptions:

- All precipitation files (.pre) would be structured the same. For example, I assumed that the flags such as 'Grid-ref=', 'Years=' and 'Missing=' would be the same for all .pre files.
- Although the example file provided can be read into memory without issues, I assumed that different time periods could be selected to export the precipitation file (e.g. more than ten years) so I chose a solution that would iterate over the file instead.
- All measurements are in millimetres.

To extract the relevant data, I used a combination of regex and string methods to transform the information into a JSON-like list of dictionaries (as shown in the example below).

```python
example_data = [
    {
        "Xref": 1,
        "Yref": 148,
        "Date": datetime(1991, 1, 1),
        "Value": 320
    },
    {
        "Xref": 1,
        "Yref": 148,
        "Date": datetime(1991, 2, 1),
        "Value": 199
    }
]
```

Although this file did not appear to have any missing data, I made the assumption that that could be possible for other precipitation files, so this solution includes substituting the missing value flagged at the top of the file with None.

I chose to output the data into a sqlite database as this was the simplest, 'on the fly' option to demonstrate how it could be written to a database. I also chose to export the data to a zipped json file as this can be transported between different systems easily.

I have included a 'resources' folder containing the example file stored on the JBA Software website and the outputs from the program run by me. The outputs are:

- precip.db - the sqlite database
- precip.zip - the json file

The sqlite database can be viewed for free online at [SQLViewer](https://inloop.github.io/sqlite-viewer/).

## Project setup

This package uses Python (version 3.9 onwards). All modules used are standard Python modules except for `pandas`. `pandas v1.4.2` was used to develop this package.

The package can be run by opening a terminal in the top level directory (i.e. the same directory as the README.md file) and running:

`python -m precip`

The package can also be run by executing the __main__.py script in an IDE.

When the package is run, it will first ask you to enter the path of the precipitation file to be transformed. The full filepath, including extension, should be entered without quotation marks. The script will then ask for a location to save the output files. Again, this should be the full filepath to a directory of your choice without quotation marks.

If the package executes successfully, you will see a message telling you the data has been written to the database successfully.
