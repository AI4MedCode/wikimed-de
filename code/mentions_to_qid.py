'''
Task: map mention URL with QID
Ressources: mention_url.csv
            wiki_id_qid.csv
Outputs: mentions_qids.csv, a mapping of mention URL and QID
'''

import pandas as pd
import os

current_directory = os.getcwd().replace('code', '')
data_path = os.path.join(current_directory, 'data')
output_path = os.path.join(current_directory, 'outputs')

df_mention = pd.read_csv(os.path.join(output_path, 'mention_url.csv'))
df_qid = pd.read_csv(os.path.join(output_path, 'wiki_id_qid.csv'))

df_mention_valid = df_mention[df_mention['page id']!=0.0]
merged_df = pd.merge(df_mention_valid, df_qid, on='page id', how='left')
merged_df_notna = merged_df[merged_df['qid'].notna()]

merged_df_notna.to_csv(os.path.join(output_path, 'mentions_qids.csv'), index=False)