from algorithms.datafly import datafly_anonymize
from .mondrian import classic_mondrian_anonymize
from .basic_mondrian import basic_mondrian_anonymize, read_tree, mondrian_ldiv_anonymize
from .clustering_based import cluster_based_anonymize
from .top_down_greedy import tdg_anonymize
from utils.types import AnonMethod

def k_anonymize(anon_params):

    if anon_params["name"] == AnonMethod.CLASSIC_MONDRIAN:
        return classic_mondrian_anonymize(
            anon_params["value"], 
            anon_params["data"], 
            anon_params["qi_index"], 
            anon_params['mapping_dict'],
            anon_params['is_cat'],
            relax=False)

    if anon_params["name"] == AnonMethod.BASIC_MONDRIAN:
        return basic_mondrian_anonymize(
            anon_params["value"], 
            anon_params["att_trees"], 
            anon_params["data"], 
            anon_params["qi_index"], 
            anon_params["sa_index"])

    if anon_params["name"] == AnonMethod.MONDRIAN_LDIV:
        return mondrian_ldiv_anonymize(
            anon_params["value"], 
            anon_params["att_trees"], 
            anon_params["data"], 
            anon_params["qi_index"], 
            anon_params["sa_index"])

    if anon_params["name"] == AnonMethod.CLUSTER:
        return cluster_based_anonymize(
            anon_params["value"], 
            anon_params["att_trees"], 
            anon_params["data"], 
            anon_params["qi_index"], 
            anon_params["sa_index"], 
            type_alg='kmember')

    if anon_params["name"] == AnonMethod.TOPDOWN:
        return tdg_anonymize(
            anon_params["value"], 
            anon_params["att_trees"], 
            anon_params["data"], 
            anon_params["qi_index"], 
            anon_params["sa_index"])

    if anon_params["name"] == AnonMethod.DATAFLY:
        return datafly_anonymize(
            anon_params["value"], 
            anon_params["csv_path"], 
            anon_params["qi_names"], 
            anon_params["data_name"], 
            anon_params["dgh_folder"],
            anon_params['res_folder'])