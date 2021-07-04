import os
from numpy.lib.npyio import _save_dispatcher
import pandas as pd

def convert_hierarchies():
    txt_names = [i for i in os.listdir('./data/informs') if i.endswith('txt')]
    for txt_name in txt_names:
        txt_path = os.path.join('./data/informs', txt_name)
        with open(txt_path, 'r') as f:
            data =f.read()
            lines = data.splitlines()
        
        new_name = txt_name.split('_')
        new_name = '_'.join([new_name[0], 'hierarchy', new_name[1]])

        with open(f'./data/informs/hierarchies/{new_name[:-4]}.csv', 'w+') as f:
            for line in lines:
                new_line = []
                levels = line.split(';')
                for level in levels:
                    level = level.replace(',', '~')
                    new_line.append(level)
                new_line = ';'.join(new_line)
                f.write(new_line+'\n')

def convert_csv():
    with open("./data/informs/demographics.csv", 'r') as fi, open("./data/informs/informs.csv", 'w') as fo:
        data =fi.read()
        lines = data.splitlines()

        for line in lines:
            newline = line.replace('"', '').replace(',', ';')
            fo.write(newline+'\n')  

convert_hierarchies()
    