import pandas as pd
import numpy as np


def transformDataset(dataset):
    symptons = ['disease']
    for row in range(1, len(dataset)):
        for column in range(1, len(dataset.columns)):
            if dataset[dataset.columns[column]][row] not in symptons:
                symptons.append(dataset[dataset.columns[column]][row])

    symptons.pop(4)
    zeroData = np.zeros(shape=(len(dataset), len(symptons)), dtype='int32')
    dataframe = pd.DataFrame(zeroData, columns=symptons)

    for row in range(0, len(dataset)):
        for column in range(0, len(dataset.columns)):
            if not pd.isna(dataset[dataset.columns[column]][row]):
                if column == 0:
                    dataframe.loc[row, 'disease'] = dataset[dataset.columns[column]][row]
                else:
                    dataframe.loc[row, dataset[dataset.columns[column]][row]] = 1

    dataframe.to_csv('datasets/modifiedDataset.csv', index=False)

