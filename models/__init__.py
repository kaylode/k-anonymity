import numpy as np
import pandas as pd
from .classifiers import (
    KNN, SVM, RFs, one_hot_encoding, 
    replace_generalization, embed_target)
from utils.types import ClassifierModel

def get_classifier(name, num_classes=None):
    if name == ClassifierModel.KNN:
        return KNN(num_classes)
    if name == ClassifierModel.SVM:
        return SVM()
    if name == ClassifierModel.RF:
        return RFs()

def classifier_evaluation(
    classifier_name,
    raw_csv, 
    train_index,
    val_index,
    qi_index, 
    is_cat, 
    att_trees=None,
    anon_csv = None): 

    with open(train_index, 'r') as f:
        data = f.read()
        train_indexes = [int(i) for i in data.splitlines()]

    with open(val_index, 'r') as f:
        data = f.read()
        val_indexes = [int(i) for i in data.splitlines()]

    df = pd.read_csv(raw_csv, delimiter=';')
    
    # Drop ID and Target columns (last column)
    df = df.drop(['ID'], axis=1)
    targets = list(df.iloc[:, -1])
    df = df.drop(df.columns[-1], axis=1)

    # Because we remove ID column
    qi_index = [i-1 for i in qi_index]

    # One-hot categorical values
    one_hot_df = one_hot_encoding(df, qi_index, is_cat)

    # print(one_hot_df.head())
    # One-hot target labels
    embeded_targets, label_to_idx = embed_target(targets)

    model = get_classifier(classifier_name, num_classes=len(label_to_idx))

    if anon_csv is not None:
        anon_df = pd.read_csv(anon_csv, delimiter=';')
        anon_df = anon_df.drop(['ID'], axis=1)
        anon_df = anon_df.drop(anon_df.columns[-1], axis=1)

        print("Replacing all generalized values...")
        one_hot_anon_df = replace_generalization(
            anon_df, 
            columns=list(one_hot_df.columns),
            qi_index=qi_index,
            is_cat=is_cat,
            att_trees=att_trees)

    if anon_csv is not None:
        # Train anonymized dataset
        # Split train/test dataset
        
        # For supressed value, check only if index exists in dataframe
        union = [i for i in train_indexes if i in list(one_hot_anon_df.index)]
        train_features = one_hot_anon_df.loc[union]
        train_targets = [embeded_targets[i] for i in union]
        
        # For supressed value, check only if index exists in dataframe
        union = [i for i in val_indexes if i in list(one_hot_anon_df.index)]
        val_features = one_hot_anon_df.iloc[union]
        val_targets = [embeded_targets[i] for i in union]
    
        # Fit
        print("Fitting model on anonymized dataset")
        model.fit(train_features, train_targets)

        # Evaluation
        result = model.eval(val_features, val_targets, label_to_idx.keys())
    else:
        # Train original dataset
        # Split train/test dataset
        train_features = one_hot_df.iloc[train_indexes]
        train_targets = [embeded_targets[i] for i in train_indexes]
        
        val_features = one_hot_df.iloc[val_indexes]
        val_targets = [embeded_targets[i] for i in val_indexes]
        
        # Fit
        print("Fitting model on original dataset")
        model.fit(train_features, train_targets)

        # Evaluation
        result = model.eval(val_features, val_targets, label_to_idx.keys())

    f1_score = np.round(float(result),3)
    return f1_score
