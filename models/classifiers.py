import enum
import pickle
import pandas as pd
from tqdm import tqdm
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, f1_score
from algorithms import read_tree
import numpy as np

class KNN:
    """
    K- Nearest Neighbors Classifier
    """
    def __init__(self, num_classes) -> None:
        # One vs Rest classifier
        self.model = KNeighborsClassifier(n_neighbors=num_classes)
        
    def fit(self, inputs, targets):
        self.model = self.model.fit(inputs, targets)

    def eval(self, inputs, targets, class_names=[]):
        if len(class_names) == 0:
            class_names = None
        preds = self.model.predict(inputs)
        # return classification_report(targets, preds, target_names=class_names, output_dict=True)
        return f1_score(targets, preds, labels=np.unique(preds), average='weighted')
         

    def save_model(self, path):
        pickle.dump(self.model, open(path, 'wb'))

    def load_model(self, path):
        self.model = pickle.load(open(path, 'rb'))

class SVM:
    """
    Support Vector Machine Classifier
    """
    def __init__(self) -> None:
        # One vs Rest classifier
        self.model = svm.SVC(decision_function_shape = "ovr")
        
    def fit(self, inputs, targets):
        self.model = self.model.fit(inputs, targets)

    def eval(self, inputs, targets, class_names=[]):
        if len(class_names) == 0:
            class_names = None
        preds = self.model.predict(inputs)
        return f1_score(targets, preds, labels=np.unique(preds), average='weighted')
        # return classification_report(targets, preds, target_names=class_names, output_dict=True)

    def save_model(self, path):
        pickle.dump(self.model, open(path, 'wb'))

    def load_model(self, path):
        self.model = pickle.load(open(path, 'rb'))


class RFs:
    """
    Decision Tree Classifier
    """
    def __init__(self, seed=0) -> None:
        self.model = RandomForestClassifier(
                        n_estimators=300, 
                        oob_score=True,
                        min_samples_split=5, 
                        max_depth=10, random_state=seed)
        
    def fit(self, inputs, targets):
        self.model = self.model.fit(inputs, targets)

    def eval(self, inputs, targets, class_names=[]):
        if len(class_names) == 0:
            class_names = None
        preds = self.model.predict(inputs)
        return f1_score(targets, preds, labels=np.unique(preds), average='weighted')
        # return classification_report(targets, preds, target_names=class_names, output_dict=True)

    def save_model(self, path):
        pickle.dump(self.model, open(path, 'wb'))

    def load_model(self, path):
        self.model = pickle.load(open(path, 'rb'))

def one_hot_encoding(df, qi_index, is_qi_cat):
    rows, columns = df.shape
    attributes = list(df.columns)
    is_cat_list = []
    # Get list of categorical attribute
    for idx, row in df.iterrows():
        for j, value in enumerate(row):
            if j in qi_index:
                ## If QID
                pos = qi_index.index(j)
                is_cat = is_qi_cat[pos]
            else:
                try:
                    float(value)
                    is_cat = False
                except ValueError:
                    # Is categorical attribute
                    is_cat = True
            is_cat_list.append(is_cat)
        break

    # Name of categorical attributes
    cat_attrs = [attributes[idx] for idx,i in enumerate(is_cat_list) if i]

    # One hot encoding all categorical attribtutes
    df = pd.get_dummies(df, columns=cat_attrs)
    
    return df

def embed_target(targets):
    unique_labels = set(targets)
    label_to_idx = {v:i for i, v in enumerate(unique_labels)} 
    new_targets = [label_to_idx[i] for i in targets]
    return new_targets, label_to_idx

def replace_generalization(anon_df, columns, qi_index=None, is_cat=None, att_trees=None):
    """
    Replace all generalized value to its mean
    """

    def get_non_qid_value(key, value):
        try:
            return float(value), 0
        except:
            return key+'_'+value, 1

    def get_mean(value):
        if isinstance(value, str):
            tmp = value.split('~')
            if len(tmp) == 2:
                low, high = tmp
                mean = float(low) + (float(high) - float(low))/2
                return mean
            else:
                if '*' in value:
                    low = float(value.replace('*', '0'))
                    high = float(value.replace('*', '9'))
                    return low+(high-low)/2
                elif not value.isnumeric():
                    return 0
        return float(value)

    def get_caterogical_value(key, value, att_trees=None):
        if att_trees is None:
            value_splits = value.split('~')
        else:
            value_splits = att_trees[str(value)].get_leaves_names()

        return [key+'_'+i for i in value_splits]

    tmp_list = []
    for _, row in tqdm(anon_df.iterrows()):
        atr_dict = {
            key:0 for key in columns
        }
        for atr_idx, key in enumerate(list(row.keys())):
            value = row[atr_idx]
            # If not QID, append value
            if atr_idx not in qi_index:
                new_key, is_category = get_non_qid_value(key, value)
                if is_category:
                    atr_dict[new_key] = 1
                else:
                    atr_dict[key] = new_key
                continue
            else:
                # If is QID
                # If is categorical
                qi_id = qi_index.index(atr_idx)
                if is_cat[qi_id]:
                    tmp = att_trees[qi_id] if att_trees is not None else None
                    keys = get_caterogical_value(key, value, tmp)
                    for new_key in keys:
                        atr_dict[new_key] = 1
                else:
                    # If is numeric
                    mean = get_mean(value)
                    atr_dict[key] = mean
        tmp_list.append(atr_dict)

    result_dict = {
        k:[] for k in columns
    }

    for item in tmp_list:
        for atr in result_dict.keys():
            result_dict[atr].append(item[atr])
    
    new_df = pd.DataFrame(result_dict)
    return new_df

if __name__ == '__main__':
    from datasets import get_dataset_params
    with open("./data/italia/italia_train.txt", 'r') as f:
        data = f.read()
        train_indexes = [int(i) for i in data.splitlines()]

    with open("./data/italia/italia_val.txt", 'r') as f:
        data = f.read()
        val_indexes = [int(i) for i in data.splitlines()]

    df = pd.read_csv('./data/italia/italia.csv', delimiter=';')

    anon_df = pd.read_csv('./results/italia/mondrian/italia_anonymized_2.csv', delimiter=';')
    
    ATT_NAMES = list(df.columns)

    params = get_dataset_params('italia')
    QI_INDEX = params['qi_index']
    IS_CAT = params['is_category']
    IS_CAT_TMP = [True, True, True]

    gen_path = './data/italia/hierarchies'
    ATT_TREES = read_tree(
            gen_path, 
            'italia', 
            ATT_NAMES, 
            QI_INDEX, IS_CAT_TMP)
    

    # Drop ID and Target columns (last column)
    df = df.drop(['ID'], axis=1)
    targets = list(df.iloc[:, -1])
    df = df.drop(df.columns[-1], axis=1)

    anon_df = anon_df.drop(['ID'], axis=1)
    anon_df = anon_df.drop(anon_df.columns[-1], axis=1)

    # One-hot categorical values
    one_hot_df = one_hot_encoding(df)

    print("Replacing all generalized values...")
    one_hot_anon_df = replace_generalization(
        anon_df, 
        qi_index=QI_INDEX,
        is_cat=IS_CAT,
        columns=list(one_hot_df.columns),
        att_trees=ATT_TREES)

    # One-hot target labels
    embeded_targets, label_to_idx = embed_target(targets)

    dt = KNN(num_classes=len(label_to_idx))

    # Train original dataset
    # Split train/test dataset
    train_features = one_hot_df.iloc[train_indexes]
    train_targets = [embeded_targets[i] for i in train_indexes]
    
    val_features = one_hot_df.iloc[val_indexes]
    val_targets = [embeded_targets[i] for i in val_indexes]
    
    # Fit
    dt.fit(train_features, train_targets)

    # Evaluation
    result = dt.eval(val_features, val_targets, label_to_idx.keys())

    print(result)

    # Train anonymized dataset
    # Split train/test dataset
    train_features = one_hot_anon_df.iloc[train_indexes]
    train_targets = [embeded_targets[i] for i in train_indexes]
    
    val_features = one_hot_anon_df.iloc[val_indexes]
    val_targets = [embeded_targets[i] for i in val_indexes]
    
    # Fit
    dt.fit(train_features, train_targets)

    # Evaluation
    result = dt.eval(val_features, val_targets, label_to_idx.keys())

    print(result)