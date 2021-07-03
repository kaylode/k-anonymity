
from utils.types import Dataset

def get_dataset_params(name):
    if name == Dataset.ADULT:
        QI_INDEX = [1, 2, 3, 4, 5, 6, 7, 8]
        target_var = 'salary-class'
        IS_CAT = [True, False, True, True, True, True, True, True]
        max_numeric = {"age": 50.5}
    elif name == Dataset.CMC:
        QI_INDEX = [1, 2, 4]
        target_var = 'method'
        IS_CAT = [False, True, False]
        max_numeric = {"age": 32.5, "children": 8}
    elif name == Dataset.MGM:
        QI_INDEX = [1, 2, 3, 4, 5]
        target_var = 'severity'
        IS_CAT = [True, False, True, True, True]
        max_numeric = {"age": 50.5}
    elif name == Dataset.CAHOUSING:
        QI_INDEX = [1, 2, 3, 8, 9]
        target_var = 'ocean_proximity'
        IS_CAT = [False, False, False, False, False]
        max_numeric = {"latitude": 119.33, "longitude": 37.245, "housing_median_age": 32.5,
                    "median_house_value": 257500, "median_income": 5.2035}

    return {
        'qi_index': QI_INDEX,
        'is_category': IS_CAT,
        'target_var': target_var,
        'max_numeric': max_numeric
    }