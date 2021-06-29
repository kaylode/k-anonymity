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
from utils.types import AnonMethod, Dataset

parser = argparse.ArgumentParser('K-Anonymize')
parser.add_argument('--method', type=str, default='mondrian',
                    help="K-Anonymity Method")
parser.add_argument('--k', type=int, default=2,
                    help="K-Anonymity")

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
    
    if config.project_name == Dataset.ADULT:
        QI_INDEX = [1, 2, 3, 4, 5, 6, 7, 8]
        target_var = 'salary-class'
        IS_CAT2 = [True, False, True, True, True, True, True, True]
        max_numeric = {"age": 50.5}
    elif config.project_name == Dataset.CMC:
        QI_INDEX = [1, 2, 4]
        target_var = 'method'
        IS_CAT2 = [False, True, False]
        max_numeric = {"age": 32.5, "children": 8}
    elif config.project_name == Dataset.MGM:
        QI_INDEX = [1, 2, 3, 4, 5]
        target_var = 'severity'
        IS_CAT2 = [True, False, True, True, True]
        max_numeric = {"age": 50.5}
    elif config.project_name == Dataset.CAHOUSING:
        QI_INDEX = [1, 2, 3, 8, 9]
        target_var = 'ocean_proximity'
        IS_CAT2 = [False, False, False, False, False]
        max_numeric = {"latitude": 119.33, "longitude": 37.245, "housing_median_age": 32.5,
                       "median_house_value": 257500, "median_income": 5.2035}

    QI_NAMES = list(np.array(ATT_NAMES)[QI_INDEX])
    IS_CAT = [True] * len(QI_INDEX)
    SA_INDEX = [index for index in range(len(ATT_NAMES)) if index not in QI_INDEX]
    SA_var = [ATT_NAMES[i] for i in SA_INDEX]

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

    if args.method == AnonMethod.MONDRIAN:
        anon_data = mondrian_anonymize(
            ATT_TREES, 
            raw_data, args.k, 
            path, QI_INDEX, SA_INDEX)
    elif args.method == AnonMethod.CLUSTER:
        anon_data = cluster_based_anonymize(
            ATT_TREES, 
            raw_data, args.k, 
            path, QI_INDEX, SA_INDEX, 
            'knn')
    elif args.method == AnonMethod.TOPDOWN:
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