"""Get user input from browser windows

This module contains the get_user_input() function to get the
precipitation file to be transformed and the location where the output
data will be saved."""

from tkinter import filedialog


def get_user_input():
    """Asks the user to choose a precipitation file and an output folder.

    Returns
    -------
    precip_file : str
        The filepath of the precipitation file
    output_folder : str
        The filepath to the directory where the outputs will be saved.
    """

    precip_file = filedialog.askopenfilename(title="Select the precipitation file.")
    output_folder = filedialog.askdirectory(title="Select the output location.")

    return precip_file, output_folder
