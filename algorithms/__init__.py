from .basic_mondrian import mondrian_anonymize, read_tree
from .clustering_based import cluster_based_anonymize
from .top_down_greedy import tdg_anonymize
from .utils.generalization import age, hierarchy, l1sub
from utils.types import AnonMethod

def get_anon_method(name):
    if name == AnonMethod.MONDRIAN:
        return mondrian_anonymize
    if name == AnonMethod.CLUSTER:
        return cluster_based_anonymize
    if name == AnonMethod.TOPDOWN:
        return tdg_anonymize

def k_anonymize(
    method, 
    att_trees, 
    data,
    k,
    qi_index, # quasi-identifier
    sa_index, # sensitive atribute
    **kwargs):


    return method(att_trees, data, k, qi_index, sa_index, **kwargs)