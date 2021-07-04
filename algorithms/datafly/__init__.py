import os
from .datafly import datafly

def datafly_anonymize(k, csv_path, qi_names, data_name, dgh_folder, res_folder):
    return datafly(k, qi_names, csv_path, data_name, dgh_folder, res_folder)
