# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import torch.utils.data as dt
import pandas as pd 
import numpy as np
import torch.utils.data as data_utils
import matplotlib.pyplot as plt

data_path = "../repeating_deleted_US_Videos.csv"

# data preparation
df_main = pd.read_csv(data_path, sep = ',')
#subset data for testing ,use the first 10000
df = df_main
df_features=df[['title', 'total_time', 'likes']]

print(df_features)
times = df_features["total_time"].values
likes = df_features["likes"].values

print(len(times))