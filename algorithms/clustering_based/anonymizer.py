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



def extend_result(val):
    """
    separated with ',' if it is a list
    """
    if isinstance(val, list):
        return ','.join(val)
    return val


def cluster_based_anonymize(k, att_trees, data, qi_index, sa_index, type_alg='knn', **kwargs):
    """
    Clustering-based K-anonymity
    """
    result, runtime = clustering_based_k_anon(att_trees, reorder_columns(
        copy.deepcopy(data), qi_index), k, len(qi_index), sa_index, type_alg)
    
    return restore_column_order(result, qi_index), runtime
