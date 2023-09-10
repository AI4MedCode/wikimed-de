'''
Task: mapping CUI to TUI
Ressources: MRSTY.RRF in umls-2023AA-mrconso.zip downloaded from https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html
            the description of each file can be seen on https://www.ncbi.nlm.nih.gov/books/NBK9685/
            wikidata_CUI.csv, a mapping of QID and CUI
Output: cui_tui.csv, a CSV file containing the mapping of CUI and TUI
        qid_cui_tui.csv, a CSV file consisting of QID, CUI, TUI and semantic type label.
'''

# import libraries
from tqdm import tqdm
import pandas as pd
import os

current_directory = os.getcwd().replace('code', '')
data_path = os.path.join(current_directory, 'data')
output_path = os.path.join(current_directory, 'outputs')
# reading file
file_path = os.path.join(data_path, '2023AA/META/MRSTY.RRF')

with open(file_path, 'r') as file:
    file_contents = file.read()

# mapping cui with TUI
# for example, 'C0000096|T109|A1.4.1.2.1|Organic Chemical|AT17685682|256|'
rows = []
lines = file_contents.split('\n')
for line in tqdm(lines[:-1]):
    contents = line.split('|')
    cui = contents[0]
    tui = contents[1]
    semantic_type = contents[3]
    rows.append([cui, tui, semantic_type])

df_tui = pd.DataFrame(rows, columns=['CUI', 'TUI', 'Semantic type'])
df_tui = df_tui.drop_duplicates()
df_tui.to_csv(os.path.join(output_path, 'cui_tui.csv'), index=False)

# reading wikidata_CUI.csv
df_cui = pd.read_csv(os.path.join(data_path, 'wikidata_CUI.csv'))
entity_qid = [i.split('/')[-1] for i in df_cui['entity']]
df_cui['QID'] = entity_qid

# merging these two files can filter out the CUIs that do not have a corresponding TUI
# thus keep only the CUIs up to date
df_merge = pd.merge(df_cui, df_tui, on='CUI')

print('The number of CUIs using MRSTY.RRF: ', len(list(set(list(df_tui['CUI'])))))
print('The number of CUIs using Sparql: ', len(list(set(list(df_cui['CUI'])))))
print('The number of CUIs extracting by Sparql that have a corresponding TUI: ', len(list(set(list(df_merge['CUI'])))))

# saving csv
df_merge.to_csv(os.path.join(output_path, 'qid_cui_tui.csv'), index=False)