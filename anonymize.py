from utils.types import AnonMethod
import os
import argparse
import numpy as np
import pandas as pd

from configs import Config
from algorithms import (
        k_anonymize,
        read_tree)
from datasets import get_dataset_params
from utils.data import read_raw, write_anon, numberize_categories

parser = argparse.ArgumentParser('K-Anonymize')
parser.add_argument('--method', type=str, default='mondrian',
                    help="K-Anonymity Method")
parser.add_argument('--k', type=int, default=2,
                    help="K-Anonymity")

class Anonymizer:
    def __init__(self, args, config):
        self.method = args.method
        assert self.method in ["mondrian", "topdown", "cluster", "mondrian_ldiv", "classic_mondrian"]
        self.k = args.k
        self.data_name = config.project_name
        
        # Data path
        self.path = os.path.join('data', config.project_name)  # trailing /

        # Dataset path
        self.data_path = os.path.join(self.path, config.csv_path)

        # Generalization hierarchies path
        self.gen_path = os.path.join(
            self.path,
            'hierarchies')  # trailing /

        # folder for all results
        res_folder = os.path.join(
            'results', 
            config.project_name, 
            self.method)

        # path for anonymized datasets
        self.anon_folder = os.path.join(res_folder, 'anon_dataset')  # trailing /
        
        # path for pickled numeric values
        self.numeric_folder = os.path.join(res_folder, 'numeric')

        os.makedirs(self.anon_folder, exist_ok=True)
        os.makedirs(self.numeric_folder, exist_ok=True)

    def anonymize(self):
        data = pd.read_csv(self.data_path, delimiter=';')
        ATT_NAMES = list(data.columns)
        
        data_params = get_dataset_params(self.data_name)
        QI_INDEX = data_params['qi_index']
        IS_CAT2 = data_params['is_category']

        QI_NAMES = list(np.array(ATT_NAMES)[QI_INDEX])
        IS_CAT = [True] * len(QI_INDEX)
        SA_INDEX = [index for index in range(len(ATT_NAMES)) if index not in QI_INDEX]
        SA_var = [ATT_NAMES[i] for i in SA_INDEX]

        ATT_TREES = read_tree(
            self.gen_path, 
            self.numeric_folder, 
            self.data_name, 
            ATT_NAMES, 
            QI_INDEX, IS_CAT)

        raw_data, header = read_raw(
            self.path, self.numeric_folder, 
            self.data_name, 
            QI_INDEX, IS_CAT)

        anon_params = {
            "name" :self.method,
            "att_trees" :ATT_TREES,
            "value" :self.k,
            "qi_index" :QI_INDEX, 
            "sa_index" :SA_INDEX
        }

        if self.method == AnonMethod.CLASSIC_MONDRIAN:
            mapping_dict,raw_data = numberize_categories(raw_data, QI_INDEX, SA_INDEX, IS_CAT2)
            anon_params.update({'mapping_dict': mapping_dict})
            anon_params.update({'is_cat': IS_CAT2})

        anon_params.update({'data': raw_data})

        print(f"Anonymize with {self.method}")
        anon_data, ncp_score, runtime = k_anonymize(anon_params)

        nodes_count = write_anon(
            self.anon_folder, 
            anon_data, 
            header, 
            self.k, 0, 
            self.data_name)

        print(f"NCP score: {ncp_score}%")
        print(f"Time execution: {runtime}s")

def main(args, config):
    anonymizer = Anonymizer(args, config)
    anonymizer.anonymize()
    

if __name__ == '__main__':
    args = parser.parse_args()
    config = Config("./configs/configs.yaml")
    main(args, config)