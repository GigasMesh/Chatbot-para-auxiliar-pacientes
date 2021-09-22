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

    def removeRowByElement(self, element, column=None, all=True):
        if not column or column not in self.dataset.columns:
            column = self.dataset.columns[0]
        for row in range(len(self.dataset)):
            if self.dataset[column][row] == element:
                self.dataset = self.dataset.drop(row, axis=0)
                if not all:
                    break

    def removeColumnByName(self, name):
        for column in self.dataset.columns:
            print(column, name)
            if column.replace(" ", "") == name:
                self.dataset.drop(column, axis=1, inplace=True)

    def renameColumnElement(self, element, name):
        for column in self.dataset.columns:
            if column.replace(" ", "") == element:
                print(column, name)
                self.dataset.rename({column: name}, axis=1, inplace=True)

    def removeRowByOnes(self):
        for row in range(len(self.dataset)):
            numberOfOnes = 0
            for column in self.dataset.columns:
                if self.dataset[column][row] == 1:
                    numberOfOnes += 1
            if numberOfOnes <= 2:
                self.dataset.drop(row, axis=0, inplace=True)
