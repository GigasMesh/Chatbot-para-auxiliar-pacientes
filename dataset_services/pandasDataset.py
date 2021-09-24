import pandas as pd
import numpy as np


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

    def getRanking(self):
        symptons = []
        numbers = np.zeros(len(self.dataset.columns) - 1)
        for column in range(1, len(self.dataset.columns)):
            symptons.append(self.dataset.columns[column])
            for row in range(len(self.dataset)):
                if self.dataset[self.dataset.columns[column]][row] == 1:
                    numbers[column-1] += 1
        id = np.argsort(numbers)
        symptons = np.array(symptons)
        return symptons[id[::-1]]

    def getCorrelatedSymptoms(self, symptom, list):
        symptoms = []
        for row in range(len(self.dataset)):
            correlated = True
            for index in list:
                if self.dataset[index][row] != 1:
                    correlated = False
            if self.dataset[symptom][row] != 1:
                correlated = False
            if correlated:
                for column in self.dataset.columns:
                    if column != symptom:
                        if self.dataset[column][row] == 1 and column not in symptoms and column not in list:
                            symptoms.append(column)
        return symptoms

