from dataset_services import PandasDataset
from dataset_services import transformDataset

pandasDataset = PandasDataset('datasets/dataset.csv')
transformDataset(pandasDataset.dataset)
pandasDataset = PandasDataset('datasets/modifiedDataset.csv')
# pandasDataset.saveDataset()
