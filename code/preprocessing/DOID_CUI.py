'''
Task: mapping DOID to TUI
Ressources: doid.json downloaded from https://github.com/DiseaseOntology/HumanDiseaseOntology/blob/main/src/ontology/releases/doid.json
            cui_tui.csv, a mapping of CUI and TUI   
            wikidata_DOID.csv, a mapping of QID and DOID 
Output: doid_cui.csv, a CSV file consisting of DOID and CUI
        doid_cui_tui.csv, a CSV file containing of the mapping of DOID, CUI and TUI
        qid_doid.csv, a CSV file consisting of QID and DOID
'''

# import libraries
import json
from tqdm import tqdm
import pandas as pd
import os

current_directory = os.getcwd().replace('code', '')
data_path = os.path.join(current_directory, 'data')
output_path = os.path.join(current_directory, 'outputs')

# reading file
with open(os.path.join(data_path, 'doid.json'), 'r', encoding='utf-8') as jsonf:
  jsonarray = json.load(jsonf)

# mapping DOID with CUI
doid_cui = []
for i in jsonarray['graphs']:
    nodes = i['nodes']
    for node in tqdm(nodes):
        try:
            doid = node['id'].split('/')[-1].split('_')[0]+':'+node['id'].split('/')[-1].split('_')[1]
            meta = node['meta']['xrefs']
            for vals in meta:
                val = vals['val']
                if 'UMLS_CUI' in val:
                    cui = val.split(':')[-1]
                    doid_cui.append([doid, cui])
        except:
            pass

# writing the result to dataframe
df = pd.DataFrame(doid_cui, columns=['DOID', 'CUI'])
df = df.drop_duplicates()
df.to_csv(os.path.join(output_path, 'doid_cui.csv'), index=False)

# mapping DOID with TUI
df_tui = pd.read_csv(os.path.join(output_path, 'cui_tui.csv'))
df_merge = pd.merge(df, df_tui, on='CUI')
df_merge.to_csv(os.path.join(output_path, 'doid_cui_tui.csv'), index=False)

# splitting QID from entity links
df_doid = pd.read_csv(os.path.join(data_path, 'wikidata_DOID.csv'))
entity_qid = [i.split('/')[-1] for i in df_doid['entity']]
df_doid['QID'] = entity_qid
df_doid.to_csv(os.path.join(output_path, 'qid_doid.csv'), index=False)
        
    