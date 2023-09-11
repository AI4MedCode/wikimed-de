'''
Task: aggregate all information
The only difference between WikiMed-DE-BEL and WikiMed-DE is that we keep mentions with a unique UMLS CUI in WikiMed-DE-BEL.
Ressources: multistream_text.json
		    wiki_id_qid.csv
		    qid_cui_tui.csv
		    qid_mesh.csv
		    qid_doid.csv
		    mesh_cui_tui.csv
		    doid_cui_tui.csv
		    mentions_url_including_redirect.csv
Outputs: WikiMed-DE-BEL.json
'''

from tqdm import tqdm
import json
import pandas as pd
import time
from itertools import chain
from bs4 import BeautifulSoup
from urllib.parse import unquote
import html
import re
import os

current_directory = os.getcwd().replace('code', '')
data_path = os.path.join(current_directory, 'data')
output_path = os.path.join(current_directory, 'outputs')

start_time = time.time()

with open(os.path.join(output_path, 'multistream_text.json'), 'r', encoding='utf-8') as jsonf:
  jsondata = json.load(jsonf)

end_time = time.time()
print(f"Loading time: {end_time - start_time:.2f} seconds")

df_qid = pd.read_csv(os.path.join(output_path, 'wiki_id_qid.csv'))
df_cui = pd.read_csv(os.path.join(output_path, 'qid_cui_tui.csv'))
df_mesh = pd.read_csv(os.path.join(output_path, 'qid_mesh.csv'))
df_doid = pd.read_csv(os.path.join(output_path, 'qid_doid.csv'))
df_mesh_cui = pd.read_csv(os.path.join(output_path, 'mesh_cui_tui.csv'))
df_doid_cui = pd.read_csv(os.path.join(output_path, 'doid_cui_tui.csv'))
df_mentions_qid = pd.read_csv(os.path.join(output_path, 'mentions_url_including_redirect.csv'))
filtered_df = df_mentions_qid[df_mentions_qid['qid'].notna()]

# extract qid and cui values using Pandas
qid_dict = df_qid.set_index('page id')['qid'].to_dict()
wikicui_dict = df_cui.groupby('QID')['CUI'].apply(list).to_dict()
mesh_dict = df_mesh.set_index('QID')['MeSH_ID'].to_dict()
doid_dict = df_doid.set_index('QID')['DOID'].to_dict()
mention_dict = filtered_df.set_index('url')['qid'].to_dict()
mesh_cui_dict = df_mesh_cui.groupby('MeSH_ID')['CUI'].apply(list).to_dict()
doid_cui_dict = df_doid_cui.groupby('DOID')['CUI'].apply(list).to_dict()
tui_dict = df_cui.set_index('CUI')['TUI'].to_dict()
st_dict = df_cui.set_index('CUI')['Semantic type'].to_dict()

def extract_text_within_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    extracted_texts = []
    for tag in soup.find_all('a'):
        url = re.findall(r'href="(.*?)"', str(tag))
        extracted_texts.append((url[0], tag.text, text.find(str(tag)), text.find(str(tag)) + len(tag.text)))
        text = text.replace(str(tag), tag.text)
    return extracted_texts

jsonarray = []
for i in tqdm(jsondata):
    decoded_text = html.unescape(i['text'])
    decoded_tag = unquote(decoded_text)
    decoded_tag = re.sub(r'<a href=".*?">(.*?)</a>', r'\1', decoded_tag)
    mentions = extract_text_within_tags(decoded_text)
    updated_mentions = []
    for url, mention, start, end in mentions:
        link = 'https://de.wikipedia.org/wiki/' + url
        qid_m = mention_dict.get(link, 'None') 
        wcui_m = list(set(wikicui_dict.get(qid_m, [])))
        mesh_m = mesh_dict.get(qid_m, 'None')
        mesh_cui_m = list(set(mesh_cui_dict.get(mesh_m, [])))
        doid_m = doid_dict.get(qid_m, 'None')
        doid_cui_m = list(set(doid_cui_dict.get(doid_m, [])))
        if len(wcui_m) == 1:
            cui_m = wcui_m[0]
            tui_m = tui_dict.get(cui_m, 'None')
            st_m = st_dict.get(cui_m, 'None')
        elif len(wcui_m) < 1:
            if len(mesh_cui_m) == 1:
                cui_m = mesh_cui_m[0]
                tui_m = tui_dict.get(cui_m, 'None')
                st_m = st_dict.get(cui_m, 'None')
            elif len(mesh_cui_m) < 1:
                if len(doid_cui_m) == 1:
                    cui_m = doid_cui_m[0]
                    tui_m = tui_dict.get(cui_m, 'None')
                    st_m = st_dict.get(cui_m, 'None')
                else:
                    cui_m = 'None'
                    tui_m = 'None'
                    st_m = 'None'
            else:
                    cui_m = 'None'
                    tui_m = 'None'
                    st_m = 'None'
        else:
            cui_m = 'None'
            tui_m = 'None'
            st_m = 'None'
        
        if cui_m != 'None':
            if start > 0 and end < len(decoded_tag) - 1:
                start_context = decoded_tag[start-1]
                end_context = decoded_tag[end]
                #print(decoded_tag[start:end])
                #print(decoded_tag[start-1:end+1])
                #print(start_context, end_context, end_context.isalpha())
                if start_context.isspace() and not end_context.isalpha():
                        dic_mention = {
                        "mention": mention,
                        "start_index": start,
                        "end_index": end,
                        "mention_link": link,
                        "qid": qid_m,
                        "cui": cui_m,
                        "tui": tui_m, 
                        "semantic_type": st_m,
                        "wikidata_cui": wcui_m, 
                        "mesh": mesh_m, 
                        "mesh_cui": mesh_cui_m,
                        "doid": doid_m,
                        "doid_cui": doid_cui_m 
                        }
                        updated_mentions.append(dic_mention)


    # replace html tags with extracted strings
    qid = qid_dict.get(int(i['id']), 'None')
    wcui = list(set(wikicui_dict.get(qid, [])))
    tui = list(set(chain.from_iterable([tui_dict.get(i, 'None') for i in wcui])))
    st = list(set(chain.from_iterable([st_dict.get(i, 'None') for i in wcui])))
    mesh = mesh_dict.get(qid, 'None')
    mesh_cui = list(set(mesh_cui_dict.get(mesh, [])))
    doid = doid_dict.get(qid, 'None')
    doid_cui = list(set(doid_cui_dict.get(doid, [])))
    if len(wcui) == 1:
            cui = wcui[0]
            tui = tui_dict.get(cui, 'None')
            st = st_dict.get(cui, 'None')
    elif len(wcui) < 1:
        if len(mesh_cui) == 1:
            cui = mesh_cui[0]
            tui = tui_dict.get(cui, 'None')
            st = st_dict.get(cui, 'None')
        elif len(mesh_cui) < 1:
            if len(doid_cui) == 1:
                cui = doid_cui[0]
                tui = tui_dict.get(cui, 'None')
                st = st_dict.get(cui, 'None')
            else:
                cui = 'None'
                tui = 'None'
                st = 'None'
        else:
                cui = 'None'
                tui = 'None'
                st = 'None'
    else:
        cui = 'None'
        tui = 'None'
        st = 'None'
    dic = {
        "id": i['id'],
        "url": i['url'],
        "title": i['title'],
        "text": decoded_tag,
        "qid": qid, 
        "cui": cui,
        "tui": tui, 
        "semantic_type": st,
        "wikidata_cui": wcui, 
        "mesh": mesh, 
        "mesh_cui": mesh_cui,
        "doid": doid,
        "doid_cui": doid_cui,
        "mentions": updated_mentions
    }
    jsonarray.append(dic)
    #break
            
def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

    return obj
    
with open(os.path.join(output_path, 'WikiMed-DE-BEL.json'), 'w', encoding='utf-8') as jsonf:
  jsonString = json.dumps(jsonarray, indent=4, ensure_ascii=False, default=serialize_sets)
  jsonf.write(jsonString)