import pandas as pd
''' Outputs a file with no duplicates and total video length'''

# nltk.downloader()
columns = ['video_id', 'trending_date', 'title', 'views', 'likes', 'dislikes', 'comment_count', 'sec', 'min', 'hour','publish_time']
df = pd.read_csv('US_length.csv', usecols=columns)

uniq = df['title'].unique()

df_extract = pd.DataFrame()
for i in uniq:
    cur_df = df.loc[df['title'] == i]
    max_view = max(cur_df['views'].tolist())
    cur_df = cur_df[cur_df.views == max_view]
    df_extract = df_extract.append(cur_df, sort=False,ignore_index=True)
print("Done")
secs = df_extract['sec'].values
mins = df_extract['min'].values
hours = df_extract['hour'].values
total_time = [s+60*m+3600*h for s,m,h in zip(secs, mins, hours)]
df_extract['total_time'] = total_time
df_extract = df_extract.drop(['sec', 'min', 'hour'], axis = 1)
df_extract.to_csv('./repeating_deleted_US_Videos.csv')