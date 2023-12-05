import pandas as pd


class MyCSV:
    def __init__(self):
        self.data = pd.read_csv(
            '../AgeDataset-V1.csv',
            delimiter=',')