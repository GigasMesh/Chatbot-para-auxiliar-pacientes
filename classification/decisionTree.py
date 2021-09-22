from sklearn import tree
from dataset_services import PandasDataset

class DecisionTree:
    def __init__(self):
        pandasDataset = PandasDataset('../dataset_services/datasets/modifiedDataset.csv')

        columns = pandasDataset.dataset.columns
        columns = columns[1:]
        x = pandasDataset.dataset[columns]
        y = pandasDataset.dataset['doenca']

        self.clf = tree.DecisionTreeClassifier()
        self.clf = self.clf.fit(x, y)

    def classify(self, symptoms):
        return(self.clf.predict([symptoms]))

