import pandas as pd


class PandasDataset:
    def __init__(self, path):
        self.path = path

    def access_dataset(self):
        dataset = pd.read_csv(self.path)
        return dataset
