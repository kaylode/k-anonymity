from utils.types import AnonMethod
import os
import argparse
import numpy as np
import pandas as pd
from metrics import NCP, DM, CAVG

from algorithms import (
        k_anonymize,
        read_tree)
from datasets import get_dataset_params
from utils.data import read_raw, write_anon, numberize_categories

parser = argparse.ArgumentParser('K-Anonymize')
parser.add_argument('--method', type=str, default='mondrian',
                    help="K-Anonymity Method")
parser.add_argument('--k', type=int, default=2,
                    help="K-Anonymity or L-Diversity")
parser.add_argument('--dataset', type=str, default='adult',
                    help="Dataset to anonymize")

class Anonymizer:
    def __init__(self, args):
        self.method = args.method
        assert self.method in ["mondrian", "topdown", "cluster", "mondrian_ldiv", "classic_mondrian", "datafly"]
        self.k = args.k
        self.data_name = args.dataset
        self.csv_path = args.dataset+'.csv'

        # Data path
        self.path = os.path.join('data', args.dataset)  # trailing /

        # Dataset path
        self.data_path = os.path.join(self.path, self.csv_path)

        # Generalization hierarchies path
        self.gen_path = os.path.join(
            self.path,
            'hierarchies')  # trailing /

        # folder for all results
        res_folder = os.path.join(
            'results', 
            args.dataset, 
            self.method)

        # path for anonymized datasets
        self.anon_folder = res_folder  # trailing /
        
        os.makedirs(self.anon_folder, exist_ok=True)

    def anonymize(self):
        data = pd.read_csv(self.data_path, delimiter=';')
        ATT_NAMES = list(data.columns)
        
        data_params = get_dataset_params(self.data_name)
        QI_INDEX = data_params['qi_index']
        IS_CAT2 = data_params['is_category']

        QI_NAMES = list(np.array(ATT_NAMES)[QI_INDEX])
        IS_CAT = [True] * len(QI_INDEX) # is all cat because all hierarchies are provided
        SA_INDEX = [index for index in range(len(ATT_NAMES)) if index not in QI_INDEX]
        SA_var = [ATT_NAMES[i] for i in SA_INDEX]

        ATT_TREES = read_tree(
            self.gen_path, 
            self.data_name, 
            ATT_NAMES, 
            QI_INDEX, IS_CAT)

        raw_data, header = read_raw(
            self.path, 
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

        if self.method == AnonMethod.DATAFLY:
            anon_params.update({
                'qi_names': QI_NAMES,
                'csv_path': self.data_path,
                'data_name': self.data_name,
                'dgh_folder': self.gen_path,
                'res_folder': self.anon_folder})

        anon_params.update({'data': raw_data})

        print(f"Anonymize with {self.method}")
        anon_data, runtime = k_anonymize(anon_params)

        # Write anonymized table
        if anon_data is not None:
            nodes_count = write_anon(
                self.anon_folder, 
                anon_data, 
                header, 
                self.k, 
                self.data_name)

        if self.method == AnonMethod.CLASSIC_MONDRIAN:
            ncp_score, runtime = runtime
        else:
            # Normalized Certainty Penalty
            ncp = NCP(anon_data, QI_INDEX, ATT_TREES)
            ncp_score = ncp.compute_score()

        # Discernibility Metric

        raw_dm = DM(raw_data, QI_INDEX, self.k)
        raw_dm_score = raw_dm.compute_score()

        anon_dm = DM(anon_data, QI_INDEX, self.k)
        anon_dm_score = anon_dm.compute_score()

        # Average Equivalence Class

        raw_cavg = CAVG(raw_data, QI_INDEX, self.k)
        raw_cavg_score = raw_cavg.compute_score()

        anon_cavg = CAVG(anon_data, QI_INDEX, self.k)
        anon_cavg_score = anon_cavg.compute_score()

        print(f"NCP score (lower is better): {ncp_score:.3f}")
        print(f"CAVG score (near 1 is better): BEFORE: {raw_cavg_score:.3f} || AFTER: {anon_cavg_score:.3f}")
        print(f"DM score (lower is better): BEFORE: {raw_dm_score} || AFTER: {anon_dm_score}")
        print(f"Time execution: {runtime:.3f}s")

        return ncp_score, raw_cavg_score, anon_cavg_score, raw_dm_score, anon_dm_score


def main(args):
    anonymizer = Anonymizer(args)
    anonymizer.anonymize()
    

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)