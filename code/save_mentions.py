'''
Task: save all mentions appearing in German Wikipedia articles and map mention URL with Wikipedia page ID
Ressources: multistream_text.json
Outputs: mention.csv, all mention URLs
         mention_url.csv, a mapping of mention URL and Wikipedia page ID
'''

from tqdm import tqdm
import re
import json
import pandas as pd
import html
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
import os

current_directory = os.getcwd().replace('code', '')
data_path = os.path.join(current_directory, 'data')
output_path = os.path.join(current_directory, 'outputs')

with open(os.path.join(output_path, 'multistream_text.json'), 'r', encoding='utf-8') as jsonf:
  jsondata = json.load(jsonf)

link_pattern = re.compile(r'<a.*?>(.*?)</a>')
# Initialize the list to store all urls
urls_list = []
# Iterate over the jsondata
for i in tqdm(jsondata):
    # Decode html and unquote
    decoded_text = unquote(html.unescape(i['text']))
    decoded_tag = unquote(decoded_text)
    
    matches = link_pattern.findall(decoded_text)
    # Find all url
    urls = re.findall(r'&lt;a href="(.*?)"&gt;', i['text'])
    links = ['https://de.wikipedia.org/wiki/' + result for result in urls]
    # Append the url to list
    for j, k in zip(matches, links):
        urls_list.append([j, k])
    
df = pd.DataFrame(urls_list, columns=['mention', 'url'])
df = df.drop_duplicates()
df.to_csv(os.path.join(output_path, 'mention.csv'), index=False)

def get_curid_from_wikipedia_url(link):
    time.sleep(1)
    keyword = link.split('/')[-1]
    url = 'https://de.wikipedia.org/w/index.php?title='+keyword+'&action=info'
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        if response.status_code == 200:
            # Parse the HTML content
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
                curid = soup.find('table', class_='wikitable mw-page-info').text
                curid = curid.partition('Seitenkennnummer')[2].split()[0]
                return link, curid, 200
            except:
                return link, None, 200

        else:
            if response.status_code == 429:
                print(f"Error occurred while fetching {url}: Status Code {response.status_code}")
            return link, None, response.status_code
    except:
        #print(f"Error occurred while fetching {url}: No response")
        return link, None, None
    
def fetch_data_concurrently(urls):
    with ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(get_curid_from_wikipedia_url, urls), total=len(urls)))
    return results

urls = list(df['url'])
# Fetch data concurrently with a delay of 1 second between requests
results = fetch_data_concurrently(urls)

rows = []
for url, page_id, error in results:
    rows.append([url, page_id, error])
df1 = pd.DataFrame(rows, columns=['url', 'page id', 'error'])
merged_df = pd.merge(df1, df, on='url', how='left')
merged_df.to_csv(os.path.join(output_path, 'mention_url.csv'), index=False)
