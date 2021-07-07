
import numpy as np
import matplotlib.pyplot as plt
from argparse import Namespace
from anonymize import Anonymizer


def sub_plot(result, dataset, methods):

    fig, axis = plt.subplots(nrows = 3, ncols = 6, figsize = (30, 20))

    metrics = ['ncp', 'cav', 'dm']
    lcolors = ['orange', 'deepskyblue', 'limegreen', 'magenta']

    label_x = ['adult', 'cahousing', 'cmc', 'mgm', 'informs', 'italia']
    label_y = ['Normalized\nCertainty', 'Average\nEquivalence', 'Discernibility\nMetric']

    
    for row, metric in enumerate(metrics):
        for col, data in enumerate(dataset):
            sub_data = result[ (data == result['data']) ]
            for i, method in enumerate(methods):
                sub = sub_data[ (method == sub_data['method'])]
                axis[row, col].plot(sub['k'], sub[metric], color = lcolors[i])

    for ax, col in zip(axis[0], label_x):
        ax.set_title(col.upper())

    for ax, row in zip(axis[:,0], label_y):
        ax.set_ylabel(row, size = 12)
        ax.get_yaxis().set_label_coords(-0.4, 0.5)
    
    plt.subplots_adjust(0.075, 0.05, 0.97, 0.95, 0.4, 0.25)
    plt.show()


def plot_metric():
    col = ["data", "method", "k", "ncp", "cav", "dm"]
    result = np.genfromtxt("metric_result", names = col, dtype = None)
    dataset = np.unique(result['data'])
    methods = np.unique(result['method'])
    sub_plot(result, dataset, methods)



def run_anon_data():
    methods = ['mondrian', 'classic_mondrian', 'mondrian_ldiv', 'topdown', 'cluster', 'datafly']
    dataset = ['adult', 'cahousing', 'cmc', 'mgm', 'informs', 'italia']
    k_array = [2, 5, 10, 20, 50, 100]

    output = open("metric_result", "w")

    for data in dataset:
        for method in methods[:-2]:
            for k in k_array:
                args = Namespace()
                args.method = method
                args.dataset = data
                args.k = k
                anonymizer = Anonymizer(args)
                ncp, cav_b, cav_a, dm_b, dm_a = anonymizer.anonymize()
                result = f'{data} {method} {k} {ncp:.3f} {cav_a:.3f} {dm_a:.3f}'
                output.write(result + '\n')
    
    output.close()


plot_metric()