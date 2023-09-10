'''
We extracted the multistream pages using wikiextractor
Although we extracted the json version
The extracted data is txt and is split into several files
But the text in each txt file is in the form of json data
So, we aggregated all extracted files into a json file here

Ressources: the extracted file using wikiextractor
Output: multistream.json, a json file containing all German Wikipedia articles
''' 

import os
from itertools import chain
from tqdm import tqdm
import json

current_directory = os.getcwd().replace('code', '')
data_path = os.path.join(current_directory, 'data')
output_path = os.path.join(current_directory, 'outputs')

text_path = os.path.join(data_path, 'text')

folders = [os.path.join(text_path, f) for f in os.listdir(text_path) if '.' not in f]
print('The number of folders: ', len(folders))
files = []

for folder in folders:
    file = [os.path.join(folder, f) for f in os.listdir(folder)]
    files.append(file)
files = list(chain.from_iterable(files))
print('The number of files: ', len(files))

jsonArray = []
for file in tqdm(files):
    with open(file) as f:
        jsonArray.append([json.loads(line) for line in f.readlines()])

jsonArray = list(chain.from_iterable(jsonArray))

print('The number of JSON files: ', len(jsonArray))
def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

    return obj

with open(os.path.join(output_path, 'multistream.json'), 'w', encoding='utf-8') as jsonf:
  jsonString = json.dumps(jsonArray, indent=4, ensure_ascii=False, default=serialize_sets)
  jsonf.write(jsonString)