# -*- coding: utf-8 -*-
"""
run basic_mondrian with given parameters
"""
import copy
from pdb import run
import sys
import os

from .mondrian import mondrian, mondrian_l_diversity

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


def basic_mondrian_anonymize(k, att_trees, data, qi_index, sa_index, **kwargs):
    """
    Basic Mondrian with K-Anonymity
    """
    result, runtime = mondrian(
        att_trees, 
        reorder_columns(copy.deepcopy(data), qi_index), 
        k, len(qi_index), sa_index)

    return restore_column_order(result, qi_index), runtime

def mondrian_ldiv_anonymize(l, att_trees, data, qi_index, sa_index):
    """
    Basic Mondrian with L-diversity
    """
    
    result, runtime = mondrian_l_diversity(
        att_trees, 
        reorder_columns(copy.deepcopy(data), qi_index), 
        l, len(qi_index), sa_index)
    
    
    return restore_column_order(result, qi_index), runtime
