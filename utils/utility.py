# -*- coding: utf-8 -*-

import csv

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics, svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.neighbors import KNeighborsClassifier
from xgboost.sklearn import XGBClassifier


def show_classifier_metrics(y_train, pred_train, y_test, pred_test, print_classification_report=True, print_confusion_matrix=True):
    if print_confusion_matrix:
        plt.figure(figsize=(6, 4))
        sns.heatmap(metrics.confusion_matrix(y_train, pred_train), annot=True, fmt='d', cmap="viridis")
        plt.title('Confusion matrix | Training data')
        plt.show()
        plt.figure(figsize=(6, 4))
        sns.heatmap(metrics.confusion_matrix(y_test, pred_test), annot=True, fmt='d', cmap="viridis")
        plt.title('Confusion matrix | Test data')
        plt.show()
    if print_classification_report:
        print('Classification report | Test data')
        print(metrics.classification_report(y_test, pred_test))
    print('Accuracy | Test data: %f%%' % (metrics.accuracy_score(y_test, pred_test) * 100))
    print('Accuracy | Training data: %f%%' % (metrics.accuracy_score(y_train, pred_train) * 100))


def get_classifier_metrics(y_test, pred_test):
    precision, recall, f1_score, support = score(
        y_test, pred_test, average='macro')
    acc = metrics.accuracy_score(y_test, pred_test) * 100
    return acc, precision, recall, f1_score


def zero_rule_baseline(y):
    baseline = max(y.value_counts() * 100) / len(y)
    return baseline


def create_classifier(classifier, dataset):
    if classifier == 'rf':
        clf = RandomForestClassifier(n_estimators=300, oob_score=True,
                                     min_samples_split=5, max_depth=10, random_state=10)
    elif classifier == 'svm':
        clf = svm.LinearSVC(max_iter=1000, dual=False)
    elif classifier == 'knn':
        clf = KNeighborsClassifier(n_neighbors=10)
    elif classifier == 'xgb':
        param = {}
        if dataset == 'cahousing' or dataset == 'cmc':
            param['objective'] = 'multi:softmax'
            param['num_class'] = 3
        param['learning_rate'] = 0.1
        param['verbosity'] = 1
        param['colsample_bylevel'] = 0.9
        param['colsample_bytree'] = 0.9
        param['subsample'] = 0.9
        param['reg_lambda'] = 1.5
        param['max_depth'] = 5
        param['n_estimators'] = 100
        param['seed'] = 10
        clf = XGBClassifier(**param)
    else:
        print('Invalid classifier!')
    return clf


def write_results(s, ml_res, anon_method, output_path, num=''):
    if len(ml_res.acc) <= 1:
        return

    # Write results for OLA
    # Every Suppression is its own file
    if anon_method in ['ola']:
        output_path = output_path[:-4] + '_s_' + str(s) + '.csv'

    with open(
        output_path, 'w', newline=''
    ) as csvfile:  # in Python 3 the writer writes an extra blank row #https://stackoverflow.com/questions/16271236/python-3-3-csv-writer-writes-extra-blank-rows
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(zip(*ml_res))
