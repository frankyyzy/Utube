import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as dt
import pandas as pd 
import numpy as np
import torch.utils.data as data_utils
import matplotlib.pyplot as plt

## 
data_path = "./repeating_deleted_US_length.csv"
learning_rate = 0.02
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
split = 0.8
batch_size = 50
num_epochs = 100
subset_val = None