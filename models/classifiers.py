import pickle
from sklearn import tree, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

class KNN:
    """
    Support Vector Machine Classifier
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
        return classification_report(targets, preds, target_names=class_names, output_dict=True)

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
        return classification_report(targets, preds, target_names=class_names, output_dict=True)

    def save_model(self, path):
        pickle.dump(self.model, open(path, 'wb'))

    def load_model(self, path):
        self.model = pickle.load(open(path, 'rb'))


class DecisionTree:
    """
    Decision Tree Classifier
    """
    def __init__(self) -> None:
        self.model = tree.DecisionTreeClassifier()
        
    def fit(self, inputs, targets):
        self.model = self.model.fit(inputs, targets)

    def eval(self, inputs, targets, class_names=[]):
        if len(class_names) == 0:
            class_names = None
        preds = self.model.predict(inputs)
        return classification_report(targets, preds, target_names=class_names, output_dict=True)
        
    def plot_tree(self):    
        tree.plot_tree(self.model)

    def save_model(self, path):
        pickle.dump(self.model, open(path, 'wb'))

    def load_model(self, path):
        self.model = pickle.load(open(path, 'rb'))

def generate_mapping(df):
    rows, columns = df.shape
    mapping_dict = [{} for i in range(columns)]
    mapping_count = [0 for i in range(columns)]
    for idx, row in df.iterrows():
        for j, value in enumerate(row):
            try:
                float(value)
            except ValueError:
                if value not in mapping_dict[j].keys():
                    mapping_dict[j][value] = mapping_count[j]
                    mapping_count[j] += 1
    
    return mapping_dict

def embedding(df, mapping_dict):
    features = []
    targets = []
    for idx, row in df.iterrows():
        item = [mapping_dict[i][value] if value in mapping_dict[i].keys() else value for i, value in enumerate(row)]
        features.append(item[:-1])
        targets.append(item[-1])

    return features, targets

if __name__ == '__main__':
    import pandas as pd

    with open("./data/adult/adult_train.txt", 'r') as f:
        data = f.read()
        train_indexes = [int(i) for i in data.splitlines()]

    with open("./data/adult/adult_val.txt", 'r') as f:
        data = f.read()
        val_indexes = [int(i) for i in data.splitlines()]

    df = pd.read_csv('./data/adult/adult.csv', delimiter=';')

    df = df.drop(['ID'], axis=1)

    train_df = df.loc[train_indexes]
    val_df = df.loc[val_indexes]

    mapping_dict = generate_mapping(df)

    train_features, train_targets = embedding(train_df, mapping_dict)
    val_features, val_targets = embedding(val_df, mapping_dict)
    
    dt = KNN(num_classes=2)

    dt.fit(train_features, train_targets)
    result = dt.eval(val_features, val_targets, mapping_dict[-1].keys())

    print(result)