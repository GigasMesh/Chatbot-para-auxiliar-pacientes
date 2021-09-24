from sklearn import tree
from dataset_services import PandasDataset
import numpy as np

class DecisionTree:
    def __init__(self, path):
        self.pandasDataset = PandasDataset(path)

        columns = self.pandasDataset.dataset.columns
        columns = columns[1:]
        x = self.pandasDataset.dataset[columns]
        y = self.pandasDataset.dataset['doenca']

        self.clf = tree.DecisionTreeClassifier()
        self.clf = self.clf.fit(x, y)

    def classify(self, symptoms):
        return(self.clf.predict([symptoms]))

    def returnDisease(self, symtomps):
        symtomps.pop(0)
        columns = list(self.pandasDataset.dataset.columns)
        columns.pop(0)
        classifier = np.zeros(len(columns))

        for symptom in symtomps:
            for value in range(len(columns)):
                if symptom == columns[value]:
                    classifier[value] = 1

        return self.classify(classifier)
