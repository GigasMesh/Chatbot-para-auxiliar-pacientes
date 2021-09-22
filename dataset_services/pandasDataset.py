import pandas as pd


class PandasDataset:
    def __init__(self, path):
        self.path = path
        self.dataset = self.access_dataset()

    def access_dataset(self):
        dataset = pd.read_csv(self.path)
        return dataset

    def saveDataset(self):
        self.dataset.to_csv(self.path, index=False)

    def removeRowByElement(self, element, column=None):
        if not column or column not in self.dataset.columns:
            column = self.dataset.columns[0]
        for row in range(len(self.dataset)):
            if self.dataset[column][row] == element:
                self.dataset = self.dataset.drop(row, axis=0)
                break

    def displayZeroColumn(self):
        pass
