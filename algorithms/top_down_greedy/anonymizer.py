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


def tdg_anonymize(att_trees, data, k, path, qi_index, SA_index):
    "run Top_Down_Greedy_Anonymization for one time, with k=10"
    print("K=%d" % k)
    result, eval_result = Top_Down_Greedy_Anonymization(att_trees, reorder_columns(
        copy.deepcopy(data), qi_index), k, len(qi_index), SA_index)
    print("NCP %0.2f" % eval_result[0] + "%")
    print("Running time %0.2f" % eval_result[1] + "seconds")
    return restore_column_order(result, qi_index)
