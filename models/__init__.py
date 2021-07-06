import pandas as pd
from .classifiers import (
    KNN, SVM, RFs, one_hot_encoding, 
    replace_generalization, embed_target)

def classifier_evaluation(
    raw_csv, 
    anon_csv, 
    train_index,
    val_index,
    qi_index, 
    is_cat):

    with open(train_index, 'r') as f:
        data = f.read()
        train_indexes = [int(i) for i in data.splitlines()]

    with open(val_index, 'r') as f:
        data = f.read()
        val_indexes = [int(i) for i in data.splitlines()]

    df = pd.read_csv(raw_csv, delimiter=';')
    anon_df = pd.read_csv(anon_csv, delimiter=';')
    
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
        qi_index=qi_index,
        is_cat=is_cat,
        columns=list(one_hot_df.columns))

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
    print("Fitting model on original dataset")
    dt.fit(train_features, train_targets)

    # Evaluation
    result = dt.eval(val_features, val_targets, label_to_idx.keys())

    print(result)
    print("-"*20)
    # Train anonymized dataset
    # Split train/test dataset
    train_features = one_hot_anon_df.iloc[train_indexes]
    train_targets = [embeded_targets[i] for i in train_indexes]
    
    val_features = one_hot_anon_df.iloc[val_indexes]
    val_targets = [embeded_targets[i] for i in val_indexes]
    
    # Fit
    print("Fitting model on anonymized dataset")
    dt.fit(train_features, train_targets)

    # Evaluation
    result = dt.eval(val_features, val_targets, label_to_idx.keys())

    print(result)