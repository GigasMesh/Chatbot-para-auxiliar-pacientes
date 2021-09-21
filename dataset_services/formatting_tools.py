import pandas as pd
import numpy as np


def transform_dataset(dataset):
    symptons = ['disease']
    for row in range(1, len(dataset)):
        for column in range(1, len(dataset.columns)):
            if dataset[dataset.columns[column]][row] not in symptons:
                symptons.append(dataset[dataset.columns[column]][row])

    symptons.pop(4)
    zero_data = np.zeros(shape=(len(dataset) - 1, len(symptons)), dtype='int32')
    dataframe = pd.DataFrame(zero_data, columns=symptons)

    for row in range(1, len(dataset)):
        for column in range(0, len(dataset.columns)):
            if not pd.isna(dataset[dataset.columns[column]][row]):
                if column == 0:
                    dataframe.loc[row - 1, 'disease'] = dataset[dataset.columns[column]][row]
                else:
                    dataframe.loc[row - 1, dataset[dataset.columns[column]][row]] = 1

    dataframe.to_csv('datasets/modified_dataset.csv', index=False)