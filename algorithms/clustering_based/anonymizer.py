# -*- coding: utf-8 -*-
"""
run clustering_based_k_anon with given parameters
"""

import copy
import sys
import os

from .clustering_based_k_anon import clustering_based_k_anon
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.data import reorder_columns, restore_column_order

DATA_SELECT = 'a'
TYPE_ALG = 'kmember'
DEFAULT_K = 10
__DEBUG = True


def extend_result(val):
    """
    separated with ',' if it is a list
    """
    if isinstance(val, list):
        return ','.join(val)
    return val


def cluster_based_anonymize(att_trees, data, k, path, qi_index, SA_index, type_alg):
    "run clustering_based_k_anon for one time, with k=10"
    print("K=%d" % k)
    result, eval_result = clustering_based_k_anon(att_trees, reorder_columns(
        copy.deepcopy(data), qi_index), k, len(qi_index), SA_index, type_alg)
    print("NCP %0.2f" % eval_result[0] + "%")
    print("Running time %0.2f" % eval_result[1] + "seconds")
    return restore_column_order(result, qi_index)
