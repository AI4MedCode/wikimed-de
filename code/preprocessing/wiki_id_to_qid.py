'''
Task: mapping Wikipedia page id to QID
Ressources: dewiki-20230620-page_props.sql.gz downloaded from https://dumps.wikimedia.org/dewiki/20230620/
Output: wiki_id_qid.csv, a CSV file consisting of Wikipedia page id and QID
'''

# import libraries
import os
import gzip
from tqdm import tqdm
import re
import pandas as pd

# reading the archive
current_directory = os.getcwd().replace('code', '')
data_path = os.path.join(current_directory, 'data/dewiki-20230620-page_props.sql.gz')
output_path = os.path.join(current_directory, 'outputs')
with gzip.open(data_path, 'rt', errors='ignore') as f:
    text = f.read()

# extacting the item pairs
text_pairs = re.findall(r"\(.*?\)",text)

# selecting the wikibase_item item pairs e.g. (5,'wikibase_item','Q160726',NULL)
wikibase = []
for i in tqdm(text_pairs):
    if 'wikibase_item' in i:
        split_strings = i.split(',')
        qid = split_strings[2].replace("'", '')
        page_id = split_strings[0].replace('(', '')
        wikibase.append([page_id, qid])

# writing to csv
df = pd.DataFrame(wikibase, columns=['page id', 'qid'])
df.to_csv(os.path.join(output_path, 'wiki_id_qid.csv'), index=False)