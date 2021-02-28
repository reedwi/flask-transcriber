import json
import pandas as pd
from io import StringIO

with open('job5233.json') as j:
    data = json.load(j)

#speakers json values
df_speakers = pd.json_normalize(data['results']['speaker_labels']['segments'])
df_items = pd.DataFrame([val for vals in df_speakers['items'] for val in vals])

#content
df_content = pd.json_normalize(data['results']['items'])
df_content['content'] = [val[0]['content'] for val in df_content['alternatives']]

#merging speakers with content
merged_df = df_items.merge(df_content, how='right', on=['end_time', 'end_time'])

#grouping content with speakers to create a words column
merged_df['speaker_label'].fillna(method='bfill', inplace=True)
merged_df['isStatusChanged'] = merged_df['speaker_label'].shift(1, fill_value=merged_df['speaker_label'].head(1)) != merged_df['speaker_label']
merged_df['groups'] = merged_df['isStatusChanged'].cumsum()
merged_df['words'] = merged_df.groupby(['groups'])['content'].transform(lambda x : ' '.join(x))

df2 = merged_df[(merged_df['isStatusChanged'] == True)]
concat = pd.concat([merged_df.iloc[[0]], df2])
print(concat.head())


concat.to_csv(r'testing.csv')