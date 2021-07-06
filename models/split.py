import os
import argparse
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

parser = argparse.ArgumentParser("Splitting csv into train/test")
parser.add_argument('--input', '-i', type=str, help = 'Path to csv file')
parser.add_argument('--output', '-o', default=None, type=str, help = 'Path to output txt contains indexes')
parser.add_argument('--train_ratio', default=0.8, type=float, help='Size of training dataset')
parser.add_argument('--seed', default=2020, type=int, help='Random seed')

def split(args):
    df = pd.read_csv(args.input, delimiter=';')
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    skf = StratifiedShuffleSplit(
        n_splits=1, 
        train_size=args.train_ratio,
        random_state=args.seed)
    
    if args.output is None:
        args.output = os.path.dirname(args.input)

    csv_name = os.path.basename(args.input)
    csv_train_name = os.path.join(args.output, csv_name[:-4] + '_train.txt')
    csv_val_name = os.path.join(args.output, csv_name[:-4] + '_val.txt')

    for train_index, test_index in skf.split(X, y):
        with open(csv_train_name, 'w+') as f:
            for index in train_index:
                f.write(f"{index}\n")
        
        with open(csv_val_name, 'w+') as f:
            for index in test_index:
                f.write(f"{index}\n")
            

if __name__ == '__main__':
    args = parser.parse_args()

    split(args)
