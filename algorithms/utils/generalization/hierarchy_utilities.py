# -*- coding: utf-8 -*-

import csv
"""Utilities for creating/reading/writing generalization hierarchies

Hierarchies stored in csv files have following structure:
    level0;level1;level2;level3;...
    e.g.
    Bachelors;Undergraduate;Higher education
    12th;High School;Secondary education

Hierarchies used in code have the following structure:
    [   level1 dictionary,
        level2 dictionary,
        .
        .
        .
    ]
    e.g. (Each key represents a generalization of the values inside the list; 1.dict=level1, 2.dict=level2)
    education = [
        {"Undergraduate": [" Bachelors", " Some-college"],
         "High School":[" 11th", " HS-grad", " 9th", " 7th-8th", " 12th", " 10th"],
         "Professional Education":[" Prof-school", " Assoc-acdm", " Assoc-voc"],
         "Graduate":[" Masters", " Doctorate"]},

        {"Higher education": [" Bachelors", " Some-college", " Prof-school", " Assoc-acdm", " Assoc-voc", " Masters", " Doctorate"],
         "Secondary education":[" 11th", " HS-grad", " 9th", " 7th-8th", " 12th", " 10th"]}
    ]
"""


def create_gen_hierarchy(path):
    """Simple Textbased guide to create new generalization hierarchies

    :return: Created generalization hierarchy
    :rtype: list
    """
    raw_data = read_data(path, ";")

    headers = []
    for col in raw_data:
        headers.append(col[0])

    column_name = input('Select QI:  \n'+str(headers)+'\n')
    if column_name.isdigit():
        index = int(column_name)-1
    else:
        index = headers.index(column_name)

    column = raw_data[index]
    column_set = set(column[1:-1])

    levels = int(input('How many generalization level for QI '+headers[index]+'?\n'))

    gen_hier = []
    for value in column_set:
        for level in range(levels):

            gval = input('Level '+str(level)+' generalization for QI '+value+'?\n')
            try:
                gen_hier[level][gval].append(value)
            except KeyError:
                gen_hier[level].update({gval: [value]})
            except IndexError:
                gen_hier.append({gval: [value]})

    return gen_hier, headers[index]


def write_gen_hierarchy(path, gen_hier, header):
    """Write generalization hierarchy from variable into csv file

    :param gen_hier: Generalization hierarchy
    :param header: Name of QI
    :return: None
    """
    first_level = True
    index_list = []
    rows = []
    for di in gen_hier:
        for key, lists in di.items():
            for value in lists:
                if first_level:
                    index_list.append(value)
                    rows.append([value, key])
                else:
                    rows[index_list.index(value)].append(key)
        first_level = False

    with open(path+"gen_hier_" + str(header) + ".csv", "w") as output:
        for r in rows:
            output.write(';'.join(str(r)) + '\n')
    output.close()


def read_gen_hierarchy(path, header):
    """

    :param path: Path to the file containing the generalization hierarchy
    :return: Generalization hierarchy for one QI
    """
    gen_hier = []
    linecount = 0
    with open(path+'_hierarchy_'+header+'.csv', "r") as input:
        for line in input.readlines():
            values = line.rstrip().split(";")
            firstval = values[0]
            values = values[1:]
            colnum = 0
            for val in values:
                if linecount == 0:
                    gen_hier.append({})
                try:
                    gen_hier[colnum][val].append(firstval)
                except KeyError:
                    gen_hier[colnum].update({val: [firstval]})
                colnum += 1
            linecount += 1
    input.close()
    return gen_hier


def read_data(file_name: str, delimiter: str) -> list:
    """Reads dataset from a csv file

    :param file_name: Path to the csv file
    :param delimiter: Character that is used as delimiter in the csv file
    :return: 2d list: A Cell can be accessed with data[col][row]
    """
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                col_count = len(row)
                data = [[] for _ in range(col_count)]
            for col in range(col_count):
                data[col].append(row[col].strip())
            line_count += 1
    csv_file.close()
    return data
