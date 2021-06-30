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

DATA_SELECT = 'a'


def tdg_anonymize(att_trees, data, k, qi_index, sa_index, **kwargs):
    "run Top_Down_Greedy_Anonymization for one time, with k=10"
    result, eval_result = Top_Down_Greedy_Anonymization(att_trees, reorder_columns(
        copy.deepcopy(data), qi_index), k, len(qi_index), sa_index)
    print("NCP %0.2f" % eval_result[0] + "%")
    print("Running time %0.2f" % eval_result[1] + "seconds")
    return restore_column_order(result, qi_index)
