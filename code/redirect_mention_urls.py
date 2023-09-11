'''
Task: redirect the URL to new page ID
Ressources: mention_url.csv
            wiki_id_qid.csv
Outputs: mentions_url_including_redirect.csv, all mention URLs including the redirect URLs
'''

import wikipedia
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import requests
import os
# Set the language for Wikipedia queries
wikipedia.set_lang('de')
wikipedia.set_rate_limiting(True)

current_directory = os.getcwd().replace('code', '')
data_path = os.path.join(current_directory, 'data')
output_path = os.path.join(current_directory, 'outputs')
# Function to fetch Wikipedia page ids
def get_page_id(title):
    try:
        page = wikipedia.page(title=title, redirect=True, auto_suggest=False)
        return page.pageid
    except:
        return None

df_mention_url = pd.read_csv(os.path.join(output_path, 'mention_url.csv'))
df_qid = pd.read_csv(os.path.join(output_path, 'wiki_id_qid.csv'))
merged_df = pd.merge(df_mention_url, df_qid, on='page id', how='left')
merged_df_na = merged_df[merged_df['qid'].isna()]
titles = list(set(merged_df_na['mention']))

# Concurrently fetch page ids using multi-threading
with ThreadPoolExecutor() as executor:
    results = list(tqdm(executor.map(get_page_id, titles), total=len(titles)))

rows = []
for i, j in zip(titles, results):
    rows.append([i, j])

df = pd.DataFrame(rows, columns=['mention', 'new page id'])
merged_df1 = pd.merge(merged_df_na, df, on='mention', how='left')

def check_url_existence(url):
    time.sleep(1)
    try:
        response = requests.head(url)
        if response.status_code == 200:  # 200 indicates a successful request
            return 200
        else:
            if response.status_code == 429:
                print(f"Error occurred while fetching {url}: Status Code {429}")
            return response.status_code 
    except requests.RequestException:
        return None
urls = list(merged_df1['url'])  
with ThreadPoolExecutor() as executor:
    error = list(tqdm(executor.map(check_url_existence, urls), total=len(urls)))
merged_df1['new error']=error
merged_df1.to_csv(os.path.join(output_path, 'mentions_redirect_qid.csv'), index=False)

rows = []
for num, val in enumerate(tqdm(merged_df1['new error'])):
    try:
        page_id = int(merged_df1['new page id 1'][num])
    except:
        page_id = merged_df1['new page id 1'][num]
    rows.append([merged_df1['mention'][num], merged_df1['url'][num], page_id, merged_df1['new error'][num]])
df_re = pd.DataFrame(rows, columns=['mention', 'url', 'page id', 'error'])
merged_df_qid = pd.merge(df_re, df_qid, on='page id', how='left')
merged_df_nna = merged_df[merged_df['qid'].notna()]
concatenated_df = pd.concat([merged_df_nna, merged_df_qid], ignore_index=True)
concatenated_df.to_csv(os.path.join(output_path, 'mentions_url_including_redirect.csv'), index=False)