import math

import numpy as np
import pandas as pd

from tree.Tree import Tree


class MyCSV:
    def __init__(self):
        self.data = pd.read_csv(
            '../AgeDataset-V1.csv',
            delimiter=',')


my_CSV = MyCSV()
data = my_CSV.data[['Gender', 'Occupation', 'Age of death']].dropna().sample(frac=0.01, random_state=0)

percent = 0.75
data_percent = data.iloc[:int(len(data) * percent)]
other_data = data.iloc[int(len(data) * percent):]


def count_entr(param: str) -> dict:
    entr = {}
    for i in data_percent[param].unique():
        pi = len(data_percent[data_percent[param] == i]) / len(data_percent)
        if 0 < pi < 1:
            entr[i] = - (pi * math.log10(pi))

    entr = dict(sorted(entr.items(), key=lambda x: x[1], reverse=True))
    return entr


class TreeDecision:
    pi_occupation = count_entr('Occupation')

    pi_gender = count_entr('Gender')
    tree = Tree(data_percent, list(pi_gender.keys()))

    count_list = data.groupby(['Gender', 'Occupation']).size().reset_index(name='Count')
    count_list_other = other_data.groupby(['Gender', 'Occupation']).size().reset_index(name='CountOther')

    d = other_data.groupby(['Gender', 'Occupation'])['Age of death'].agg(np.average).reset_index()

    result = pd.merge(d, count_list, on=['Gender', 'Occupation'], how='left')
    result = pd.merge(result, count_list_other, on=['Gender', 'Occupation'], how='left')
