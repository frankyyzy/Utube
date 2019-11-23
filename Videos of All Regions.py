"""
 Combine all .csv files into a df with a new column specifying the region.
 Output a .csv file of useful information for all videos with specified region to a csv file
 named "Videos of All Regions.csv".

 @author: COGS108 group034
 @date 11/22/2019
"""

import pandas as pd

col = ['video_id', 'publish_time', 'views', 'likes', 'dislikes', 'comment_count',
       'comments_disabled', 'ratings_disabled', 'video_error_or_removed']
data_type = {"views": int, 'likes': int, 'dislikes': int, 'comment_count': int}

df_CA = pd.read_csv("Data/CAvideos.csv", index_col=0, encoding='UTF-8', usecols=col,
                    dtype=data_type)
df_DE = pd.read_csv("Data/DEvideos.csv", index_col=0, encoding='UTF-8', usecols=col,
                    dtype=data_type)
df_FR = pd.read_csv("Data/FRvideos.csv", index_col=0, encoding='UTF-8', usecols=col,
                    dtype=data_type)
df_GB = pd.read_csv("Data/GBvideos.csv", index_col=0, encoding='UTF-8', usecols=col,
                    dtype=data_type)
df_IN = pd.read_csv("Data/INvideos.csv", index_col=0, encoding='UTF-8', usecols=col,
                    dtype=data_type)
df_JP = pd.read_csv("Data/JPvideos.csv", index_col=0, encoding='UTF-8', usecols=col,
                    dtype=data_type)
df_KR = pd.read_csv("Data/KRvideos.csv", index_col=0, encoding='UTF-8', usecols=col,
                    dtype=data_type)
df_MX = pd.read_csv("Data/MXvideos.csv", index_col=0, encoding='UTF-8', usecols=col,
                    dtype=data_type)
df_RU = pd.read_csv("Data/RUvideos.csv", index_col=0, encoding='UTF-8', usecols=col,
                    dtype=data_type)
df_US = pd.read_csv("Data/USvideos.csv", index_col=0, encoding='UTF-8', usecols=col,
                    dtype=data_type)

region = ['Canada'] * df_CA.shape[0]
df_CA['region'] = region

region = ['Germany'] * df_DE.shape[0]
df_DE['region'] = region

region = ['France'] * df_FR.shape[0]
df_FR['region'] = region

region = ['Great Britain'] * df_GB.shape[0]
df_GB['region'] = region

region = ['India'] * df_IN.shape[0]
df_IN['region'] = region

region = ['Japan'] * df_JP.shape[0]
df_JP['region'] = region

region = ['South Korea'] * df_KR.shape[0]
df_KR['region'] = region

region = ['Mexico'] * df_MX.shape[0]
df_MX['region'] = region

region = ['Russia'] * df_RU.shape[0]
df_RU['region'] = region

region = ['United States'] * df_US.shape[0]
df_US['region'] = region

list_df = [df_CA, df_DE, df_FR, df_GB, df_IN, df_JP, df_KR, df_MX, df_RU, df_US]

df_videos = df_CA
for i in range(1, len(list_df)):
    df_videos = df_videos.append(list_df[i], ignore_index=False, sort=False)

df_videos.to_csv("Videos of All Regions.csv", encoding='utf-8', index=True)
