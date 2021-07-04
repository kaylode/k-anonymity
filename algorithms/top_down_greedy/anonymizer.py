# -*- coding: utf-8 -*-
"""
run top_down_greedy_anonymization with given argv
"""

import copy
import sys
import os

from .top_down_greedy_anonymization import \
    Top_Down_Greedy_Anonymization
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils.data import reorder_columns, restore_column_order



def tdg_anonymize(k, att_trees, data, qi_index, sa_index, **kwargs):
    """
    Top-Down Greedy Anonymization
    """

    result, runtime = Top_Down_Greedy_Anonymization(att_trees, reorder_columns(
        copy.deepcopy(data), qi_index), k, len(qi_index), sa_index)
    

    return restore_column_order(result, qi_index), runtime
