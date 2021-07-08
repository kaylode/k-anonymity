
import numpy as np
import matplotlib.pyplot as plt
from argparse import Namespace
from anonymize import Anonymizer

methods = ['mondrian', 'classic_mondrian', 'topdown'] #, 'cluster', 'datafly']
dataset = ['adult', 'cahousing', 'cmc', 'mgm', 'informs', 'italia']
k_array = [2, 5, 10, 20, 50, 100]

metrics = ['ncp', 'cav', 'dm']
lcolors = ['orange', 'deepskyblue', 'limegreen', 'magenta']

label_x = dataset
label_y = [
    'Normalized\nCertainty\n(lower is better)', 
    'Average\nEquivalence\n(lower is better)', 
    'Discernibility\nMetric\n(lower is better)']

def sub_plot(result, dataset, methods):

    fig, axis = plt.subplots(nrows = len(metrics), ncols = len(dataset), figsize = (30, 20))
    
    for row, metric in enumerate(metrics):
        for col, data in enumerate(dataset):
            sub_data = result[ (data == result['data']) ]
            for i, method in enumerate(methods):
                sub = sub_data[ (method == sub_data['method'])]
                axis[row, col].plot(sub['k'], sub[metric], color = lcolors[i], label=sub['method'][0])

    labels_handles = {
        label: handle for ax in fig.axes for handle, label in zip(*ax.get_legend_handles_labels())
    }

    fig.legend(
        labels_handles.values(),
        labels_handles.keys(),
        loc="upper center",
        ncol=len(labels_handles.values()))

    for ax, col in zip(axis[0], label_x):
        ax.set_title(col.upper())
    
    for ax in axis[-1]:
        ax.set_xlabel('k', size=10)

    for ax, row in zip(axis[:,0], label_y):
        ax.set_ylabel(row, size = 12)
        ax.get_yaxis().set_label_coords(-0.4, 0.5)
    
    plt.subplots_adjust(0.075, 0.05, 0.97, 0.95, 0.2, 0.25)
    plt.savefig('./demo/metrics')
    plt.show()


def plot_metric():
    col = ["data", "method", "k", "ncp", "cav", "dm"]
    result = np.genfromtxt("metric_result", names = col, dtype = None)
    dataset = np.unique(result['data'])
    methods = np.unique(result['method'])
    sub_plot(result, dataset, methods)



def run_anon_data():

    output = open("metric_result", "w")

    for data in dataset:
        for method in methods:
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

# run_anon_data()
plot_metric()