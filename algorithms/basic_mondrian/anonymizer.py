# -*- coding: utf-8 -*-
"""
run basic_mondrian with given parameters
"""
import copy
import sys
import os

from .mondrian import mondrian

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.data import reorder_columns, restore_column_order


DATA_SELECT = 'a'
DEFAULT_K = 10


def extend_result(val):
    """
    separated with ',' if it is a list
    """
    if isinstance(val, list):
        return ','.join(val)
    return val


def mondrian_anonymize(att_trees, data, k, path, qi_index, SA_index):
    "run basic_mondrian for one time, with k=10"
    print("K=%d" % k)
    print("Mondrian")
    result, eval_result = mondrian(att_trees, reorder_columns(
        copy.deepcopy(data), qi_index), k, len(qi_index), SA_index)
    print("NCP %0.2f" % eval_result[0] + "%")
    print("Running time %0.2f" % eval_result[1] + "seconds")
    return restore_column_order(result, qi_index)
