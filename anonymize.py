import os
import argparse
import numpy as np
import pandas as pd

from configs import Config
from algorithms import (
        mondrian_anonymize, 
        read_tree, 
        cluster_based_anonymize,
        tdg_anonymize,
        age, hierarchy, l1sub)
from utils.data import read_raw, write_anon

parser = argparse.ArgumentParser('K-Anonymize')

parser.add_argument('--method', type=str, default='mondrian',
                    help="K-Anonymity Method")
parser.add_argument('--k', type=int, default=2,
                    help="K-Anonymity")


ADULT = 'adult'
CAHOUSING = 'cahousing'
CMC = 'cmc'
MGM = 'mgm'

MONDRIAN = 'mondrian'
CLUSTER = 'cluster'
TOPDOWN = "topdown"

def main(args, config):

    # Data path
    path = os.path.join('data', config.project_name)  # trailing /

    # Dataset path
    data_path = os.path.join(path, config.csv_path)

    # Generalization hierarchies path
    gen_path = os.path.join(
        path,
        'hierarchies')  # trailing /

    # folder for all results
    res_folder = os.path.join(
        'results', 
        config.project_name, 
        args.method)

    # path for anonymized datasets
    anon_folder = os.path.join(res_folder, 'anon_dataset')  # trailing /
    
    # path for pickled numeric values
    numeric_folder = os.path.join(res_folder, 'numeric')

    os.makedirs(anon_folder, exist_ok=True)
    # os.makedirs(numeric_folder, exist_ok=True)

    data = pd.read_csv(data_path, delimiter=';')
    ATT_NAMES = list(data.columns)
    
    if config.project_name == ADULT:

        QI_INDEX = [1, 2, 3, 4, 5, 6, 7, 8]
        target_var = 'salary-class'
        IS_CAT2 = [True, False, True, True, True, True, True, True]
        max_numeric = {"age": 50.5}

        QI_NAMES = list(np.array(ATT_NAMES)[QI_INDEX])
        IS_CAT = [True] * len(QI_INDEX)
        SA_INDEX = [index for index in range(len(ATT_NAMES)) if index not in QI_INDEX]
        SA_var = [ATT_NAMES[i] for i in SA_INDEX]

        max_gen_level = [1, 4, 1, 2, 3, 2, 2, 2]
        gen_strat = [
            l1sub, age, l1sub,
            hierarchy(os.path.join(gen_path, config.project_name), 'marital-status'),
            hierarchy(os.path.join(gen_path, config.project_name), 'education'),
            hierarchy(os.path.join(gen_path, config.project_name), 'native-country'),
            hierarchy(os.path.join(gen_path, config.project_name), 'workclass'),
            hierarchy(os.path.join(gen_path, config.project_name), 'occupation')
        ]


    ATT_TREES = read_tree(
        gen_path, 
        numeric_folder, 
        config.project_name, 
        ATT_NAMES, 
        QI_INDEX, IS_CAT)

    raw_data, header = read_raw(
        path, numeric_folder, 
        config.project_name, 
        QI_INDEX, IS_CAT)

    if args.method == MONDRIAN:
        anon_data = mondrian_anonymize(
            ATT_TREES, 
            raw_data, args.k, 
            path, QI_INDEX, SA_INDEX)
    elif args.method == CLUSTER:
        anon_data = cluster_based_anonymize(
            ATT_TREES, 
            raw_data, args.k, 
            path, QI_INDEX, SA_INDEX, 
            'knn')
    elif args.method == TOPDOWN:
        anon_data = tdg_anonymize(
            ATT_TREES, 
            raw_data, args.k, 
            path, QI_INDEX, SA_INDEX)
                
    nodes_count = write_anon(
        anon_folder, 
        anon_data, 
        header, 
        args.k, 0, 
        config.project_name)

    

if __name__ == '__main__':
    args = parser.parse_args()
    config = Config("./configs/configs.yaml")
    main(args, config)