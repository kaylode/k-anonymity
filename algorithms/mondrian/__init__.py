import sys, copy, random
from .mondrian import mondrian
from utils.data import restore_column_order


def restore_num_to_cat(mapping_dict, data, qi_index, is_cat):
    new_data = []
    for record in data:
        new_record = []
        for i in range(len(record)):
            value = record[i]
            if i in qi_index:
                pos = qi_index.index(i)
                if is_cat[pos]:
                    # If only caterogical, restore back
                    tokens = value.split('~')
                    if len(tokens) > 1:
                        start = int(tokens[0])
                        end = int(tokens[1])
                        value_range = range(start, end+1)
                    else:
                        value_range = [int(tokens[0])]
                    restored_value = '~'.join([mapping_dict[pos][j] for j in value_range])
                    new_record.append(restored_value)
                else:
                    new_record.append(value)
            else:
                new_record.append(value)
        new_data.append(new_record)
    return new_data



def classic_mondrian_anonymize(k, data, qi_index, mapping_dict=None, is_cat=None, relax=False):
    """
    Classic Mondrian with no hierarchies, K-Anonymity
    """
    
    result, eval_result = mondrian(
        copy.deepcopy(data), 
        k, relax, len(qi_index))

    result_in_order = restore_column_order(result, qi_index)

    if mapping_dict is not None:
        restored = restore_num_to_cat(mapping_dict, result_in_order, qi_index, is_cat)
        result_in_order = restored

    ncp_score, runtime = eval_result

    return result_in_order, (ncp_score, runtime)