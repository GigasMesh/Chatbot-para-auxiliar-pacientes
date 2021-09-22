from dataset_services import PandasDataset
from unicodedata import normalize


pandasDataset = PandasDataset('datasets/modifiedDataset.csv')
# pandasDataset.saveDataset()
'''
file = open('datasets/symptons.txt')
for i in file:
    pandasDataset.removeColumnByName(i[0:-1])
'''

'''
file_portuguese = open('datasets/symptons_portuguese.txt', 'r')
file_english = open('datasets/symptons_english.txt', 'r')
portuguese = []
english = []
for i in file_portuguese:
    portuguese.append(normalize('NFKD', i[0:-1]).encode('ASCII','ignore').decode('ASCII'))
for i in file_english:
    english.append(normalize('NFKD', i[0:-1]).encode('ASCII','ignore').decode('ASCII'))

for i in range(len(portuguese)):
    pandasDataset.renameColumnElement(english[i], portuguese[i])
'''