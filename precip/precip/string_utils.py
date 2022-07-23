import re


def remove_whitespace(line):
    if not isinstance(line, str):
        raise TypeError("The argument passed must be a string.")
    return re.sub("\s", "", line)
