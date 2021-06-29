# -*- coding: utf-8 -*-

import math
from .hierarchy_utilities import read_gen_hierarchy


def hierarchy(path: str, qi_name: str)-> list:
    """Read QI hierarchy from file.
    Filenames follow a specific format: gen_hier_<gi_name>.csv

    :param path: Path to where the hierarchy file is stored
    :param qi_name: Name of the QI (header in dataset)
    :return: list: List of function+argument for that type of generalization
    """
    return [substitution, read_gen_hierarchy(path, qi_name)]


def age(data, level):
    """Transforms age data to a predefined generalization state.

    :param data: list or string: Data containing one or more age values
    :param level: int: Generalization step to which the data should be trasformed
    :return: List of generalized age data
    """
    # Use the generic function "segmentation" with predefined arguments
    return segmentation(data, level, 1, 100, [5, 10, 20, "*"])


def segmentation(data, level, min_num, max_num, div_list):
    """Transforms numerical data to a segementated state

    Parameters:
        data: list or string
            Data containing one or more numerical values
        level: int
            Generalization step to which the data should be trasformed
        min_num: int
            Start of numeric range
        max_num: int
            End of numeric range
        div_list: list
            Contains value in what range data should be grouped for each generalization step
    Returns:
        List of generalized numerical data
    """
    ret = []
    # Check if data is already a list/range or if it is a single value
    if not isinstance(data, list) and not isinstance(data, range):
        values = [int(data)]
    else:
        values = list(map(int, data))

    seg = div_list[level]

    # Check if the last level is not an integer segmentation and thus a substitution
    if len(div_list)-1 == level and not isinstance(seg, int):
        return l1sub(values, seg)

    groups = range(0, math.floor((max_num+1-min_num)/seg))
    div_max = min_num + seg + seg * groups[-1]

    for value in values:
        # Check if a value is bigger than the calculated max segementation value
        if value >= div_max:
            # Cut larger value to fit the segementation
            value = div_max - 1

        # Check in what group the value belongs
        for i in groups:
            b = min_num + seg * i
            e = b + seg
            if b <= value < e:
                e -= 1
                ret.append(str(b) + "-" + str(e))
                break
    return ret


def zip_code(data, level):
    """Transforms zipcode data to a predefined generalization state.

    Parameters:
        data: list or string
            Data containing one or more zipcode values
        level: int
            Generalization step to which the data should be trasformed
    Returns:
        List of generalized zipcode data
    """
    # Use the generic function "removeal" with predefined arguments
    return removeal(data, level, 1)


def removeal(data, level, steps):
    """Transforms zipcode data to a generalization state with removed characters.

    Parameters:
        data: list or string
            Data containing one or more generic values
        level: int
            Generalization step to which the data should be trasformed
        steps: int
            How many characters should be removed per level
    Returns:
        List of generalized data
    """
    ret = []
    # Check if data is already a list or if it is a single value
    if not isinstance(data, list):
        values = [data]
    else:
        values = data

    # How many characters to remove this level
    char_num = (level+1)*steps

    # Check if every character would be removed
    if char_num >= len(str(values[0])):
        return l1sub(values, level)

    for v in values:
        v = list(str(v))
        # Replace every character that gets removed with *
        for n in range(char_num):
            v[(-1-n)] = '*'
        ret.append("".join(v))
    return ret


def birthdate(data, level, min_year, max_year):
    """Transforms birthdate data to a predefined generalization state.

    Parameters:
        data: list or string
            Data containing one or more birthdate values (DD.MM.YYYY)
        level: int
            Generalization step to which the data should be trasformed
        min_year: int
            First year of dataset range
        max_year: int
            Last year of dataset range
    Returns:
        List of generalized birthdate data
    """
    ret = []
    if not isinstance(data, list):
        values = [data]
    else:
        values = data

    # Remove parts of date string
    for v in values:
        ret.append(v.split(".", level + 1)[-1])

    # If last generalization level is reached, apply segementation of the year
    if level >= 2:
        ret = list(map(int, ret))
        ret = segmentation(ret, 0, min_year, max_year, [10])

    return ret


def l1sub(data, placeholder):
    """Substitutes data with a character (default: *).

    :param data: list or string: Data containing one or more values
    :param placeholder: int or string:
                        <br />If int: Not used in code but allows to call this function with the standard (data,level) format
                        <br />If string: used to replace the default sub character *
    :return: List of generalized data
    """
    if isinstance(placeholder, int):
        sub_char = '*'
    else:
        sub_char = placeholder

    if not isinstance(data, list):
        values = [data]
    else:
        values = data

    return [sub_char]*len(values)


def substitution(data, level, wordlists):
    """Transforms birthdate data to a generalization state with substituted values.

    Parameters:
        data: list or string
            Data containing one or more values
        level: int
            Generalization step to which the data should be trasformed
        wordlists:
            List of dictionaries with subsition keys for each dataentry as values of the key
            Each dictionary represents a generalization level
    Returns:
        List of generalized data
    """
    ret = []
    if not isinstance(data, list):
        values = [data]
    else:
        values = data

    # Check if no more substitution is found
    if level > len(wordlists)-1:
        return l1sub(data, level)

    # Select right dictionary
    wordlist = wordlists[level]

    for value in values:
        # Search for value in dictionary
        for k, v in wordlist.items():
            if value in v:
                ret.append(k)
    return ret


if __name__ == '__main__':
    print("This is a module!")
    exit(1)
