# -*- coding: utf-8 -*-

import os
import pickle
from functools import cmp_to_key

from algorithms.basic_mondrian.models.gentree import GenTree
from algorithms.basic_mondrian.models.numrange import NumRange
from .utility import cmp_str

__DEBUG = False


def read_data(path, dataset, ATT_NAMES, QI_INDEX, IS_CAT, SA_INDEX):
    """
    read microda for *.txt and return read data
    """
    QI_num = len(QI_INDEX)
    data = []
    numeric_dict = []
    delimiter = ';'
    for i in range(QI_num):
        numeric_dict.append(dict())
    # or categorical attributes in intuitive order
    # here, we use the appear number
    with open(os.path.join(path, dataset + '.csv')) as data_file:
        next(data_file)
        for line in data_file:
            line = line.strip()
            # remove double spaces
            line = line.replace(' ', '')
            temp = line.split(delimiter)
            ltemp = []
            for i in range(QI_num):
                index = QI_INDEX[i]
                if IS_CAT[i] is False:
                    try:
                        numeric_dict[i][temp[index]] += 1
                    except KeyError:
                        numeric_dict[i][temp[index]] = 1
                ltemp.append(temp[index])
            for i in SA_INDEX:
                ltemp.append(temp[i])
            data.append(ltemp)
    # pickle numeric attributes and get NumRange
    for i in range(QI_num):
        if IS_CAT[i] is False:
            with open(os.path.join(path, dataset + '_' + ATT_NAMES[QI_INDEX[i]] + '_static.pickle'), 'wb') as static_file:
                sort_value = list(numeric_dict[i].keys())
                sort_value.sort(key=cmp_to_key(cmp_str))
                pickle.dump((numeric_dict[i], sort_value), static_file)
    return data


def read_tree(path, dataset, ATT_NAMES, QI_INDEX, IS_CAT):
    """read tree from data/tree_*.txt, store them in att_tree
    """
    att_names = []
    att_trees = []
    for t in QI_INDEX:
        att_names.append(ATT_NAMES[t])
    for i in range(len(att_names)):
        if IS_CAT[i]:
            att_trees.append(read_tree_file(path, dataset, att_names[i]))
    return att_trees


def read_pickle_file(path, dataset, att_name):
    """
    read pickle file for numeric attributes
    return numrange object
    """
    try:
        with open(os.path.join(path, dataset + '_' + att_name + '_static.pickle'), 'rb') as static_file:
            numeric_dict, sort_value = pickle.load(static_file)
    except OSError:
        print("Pickle file not exists!!")
        print(os.path.join(path, dataset + '_' + att_name + '_static.pickle'))
        exit(2)
    result = NumRange(sort_value, numeric_dict)
    return result


def read_tree_file(path, dataset, treename):
    """read tree data from treename
    """
    att_tree = {}
    prefix = os.path.join(path, dataset + '_hierarchy_')
    postfix = ".csv"
    with open(prefix + treename + postfix) as treefile:
        att_tree['*'] = GenTree('*')
        if __DEBUG:
            print("Reading Tree" + treename)
        for line in treefile:
            # delete \n
            if len(line) <= 1:
                break
            line = line.strip()
            temp = line.split(';')
            # copy temp
            temp.reverse()
            for i, t in enumerate(temp):
                isleaf = False
                if i == len(temp) - 1:
                    isleaf = True

                # try and except is more efficient than 'in'
                try:
                    att_tree[t]
                except KeyError:
                    att_tree[t] = GenTree(t, att_tree[temp[i - 1]], isleaf)
        if __DEBUG:
            print("Nodes No. = %d" % att_tree['*'].support)
    return att_tree
