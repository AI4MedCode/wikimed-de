'''
Task: mapping MeSH ID to CUI
Ressources: MRCONSO.RRF in umls-2023AA-mrconso.zip downloaded from https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html
            the description of each file can be seen on https://www.ncbi.nlm.nih.gov/books/NBK9685/
            cui_tui.csv, a mapping of CUI and TUI
            wikidata_MeSH_ID.csv, a CSV file of mapping QID with MeSH ID by using Sparql query
Output: mesh_cui.csv, a CSV file consisting of MeSH ID and CUI
        mesh_cui_tui.csv, a CSV file of mapping MeSH ID with CUI and TUI
        qid_mesh.csv, a CSV file consisting of QID and MeSH ID
'''

# import libraries
from tqdm import tqdm
import pandas as pd
import os

current_directory = os.getcwd().replace('code', '')
data_path = os.path.join(current_directory, 'data')
output_path = os.path.join(current_directory, 'outputs')

# reading file
file_path = os.path.join(data_path, '2023AA/META/MRCONSO.RRF')
with open(file_path, 'r') as file:
    file_contents = file.read()

# mapping MeSH ID with CUI
# for example, 'C0000005|ENG|P|L0000005|PF|S0007492|Y|A26634265||M0019694|D012711|MSH|PEP|D012711|(131)I-Macroaggregated Albumin|0|N|256|'
rows = []
lines = file_contents.split('\n')
matching = []
for line in tqdm(lines):
    if'|MSH' in line:
        columns = line.strip().split('|')
        mesh_id = columns[13]
        umls_cui = columns[0]
        matching.append([umls_cui, mesh_id])

df_mc = pd.DataFrame(matching, columns=['CUI', 'MeSH_ID'])
df_mc = df_mc.drop_duplicates()

# filtering out wrong rows (MeSH ID should contain digits)
def check_digits(row):
    if not any(char.isdigit() for char in row['MeSH_ID']):
        row['MeSH_ID'] = None
    return row

# applying the function to the DataFrame
df_mc = df_mc.apply(check_digits, axis=1)
df_mc = df_mc[df_mc['MeSH_ID'].notna()]
df_mc.to_csv(os.path.join(output_path, 'mesh_cui.csv'), index=False)

# mapping MeSH ID with CUI and TUI
df_tui = pd.read_csv(os.path.join(output_path, 'cui_tui.csv'))
df_merge = pd.merge(df_mc, df_tui, on='CUI')
df_merge.to_csv(os.path.join(output_path, 'mesh_cui_tui.csv'), index=False)

# splitting QID from entity links
df_mesh = pd.read_csv(os.path.join(data_path, 'wikidata_MeSH_ID.csv'))
entity_qid = [i.split('/')[-1] for i in df_mesh['entity']]
df_mesh['QID'] = entity_qid
df_mesh = df_mesh.apply(check_digits, axis=1)
df_mesh = df_mesh[df_mesh['MeSH_ID'].notna()]
df_mesh.to_csv(os.path.join(output_path, 'qid_mesh.csv'), index=False)

