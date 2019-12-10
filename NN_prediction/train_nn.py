import sys

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as dt
import pandas as pd 
import numpy as np
import torch.utils.data as data_utils
import matplotlib.pyplot as plt
import random

import pdb

seed=11
random.seed(seed)
torch.manual_seed(seed)

## 
data_path = "../US_length.csv"
learning_rate = 0.001
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
split = 0.7
batch_size = 32
num_epochs = 10
subset_val = None

df_main = pd.read_csv(data_path, sep = ',')
#subset data for testing ,use the first 10000
df = df_main[:subset_val] if (subset_val != None) else df_main
secs = df['sec'].values
mins = df['min'].values
hours = df['hour'].values
total_time = [s+60*m+3600*h for s,m,h in zip(secs, mins, hours)]
df['total_time'] = total_time
df_features=df[['title', 'total_time']]



df_label = pd.DataFrame()
df_label['views'] = df['views'].apply(np.log10)

# print(df_features.describe())
# print(df_label.describe())

exp_type = sys.argv[1]
assert exp_type in ["all_features", "LOO_title_length", "LOO_title_num_upper", "LOO_title_ratio_upper", "LOO_total_time", "LOO_title"]


## Make the data loader
tv_split = int(len(df_features)*split)
train_set = df_features[:tv_split]
train_label = df_label[:tv_split]
validation_set = df_features[tv_split:]
validation_label = df_label[tv_split:]

class Dataset(dt.Dataset):
    def __init__(self, feature, labels):
        self.labels = labels
        self.feature = feature
    def __len__(self):
        return(len(self.feature))
    def __getitem__(self, idx):
        cur_feature = self.feature.iloc[idx]
        cur_feature = np.array(cur_feature)
        title = cur_feature[0]
        title_length = len(title)
        title_num_upper = sum(1 for c in title if c.isupper())
        title_ratio_upper = title_num_upper / title_length
        total_time = cur_feature[1]

        views = np.array(self.labels.iloc[idx])[0]

        if exp_type == "all_features":
            features = np.array([title_length, title_num_upper, title_ratio_upper, total_time])
        elif exp_type == "LOO_title_length":
            features = np.array([1.0, title_num_upper, title_ratio_upper, total_time])
        elif exp_type == "LOO_title_num_upper":
            features = np.array([1.0, title_length, title_ratio_upper, total_time])
        elif exp_type == "LOO_title_ratio_upper":
            features = np.array([1.0, title_length, title_num_upper, total_time])
        elif exp_type == "LOO_title":
            features = np.array([1.0, 1.0, 1.0, total_time])
        elif exp_type == "LOO_total_time":
            features = np.array([1.0, title_length, title_num_upper, title_ratio_upper])
        else:
            raise ValueError("invalid exp type")
        
        return features, views


train = Dataset(train_set, train_label)
train_loader = data_utils.DataLoader(train, batch_size, shuffle = True)
test = Dataset(validation_set, validation_label)
test_loader = data_utils.DataLoader(test, batch_size, shuffle = True)

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size).float()
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, hidden_size).float()
        self.fc3 = nn.Linear(hidden_size, num_classes).float()
        
    def forward(self, x):
        # pdb.set_trace()
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.fc3(out)
        out = self.relu(out)
        return out


## Main training
if exp_type == "all_features":
    model = NeuralNet(4, 10, 1).to(device).train()
else:
    model = NeuralNet(4, 10, 1).to(device).train()
# Loss and optimizer
criterion = nn.L1Loss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)  
# Train the model
total_step = len(train_loader)
loss = torch.tensor(0.0)
loss_list_train = []
loss_list_val = []
for epoch in range(num_epochs):
    curr_epoch_loss = 0.0
    model = model.train()
    for i, (features, views) in enumerate(train_loader):
        # zero out the gradients in the optimizers
        optimizer.zero_grad()
        # Move tensors to the configured device
        features = features.to(device).float()
        views = views.to(device).float()
        outputs = model(features).reshape((-1))
        loss = criterion(outputs, views)
        curr_epoch_loss+=loss.data.item()
        loss.backward()
        optimizer.step()
    curr_epoch_loss /= len(train)
    loss_list_train.append(curr_epoch_loss)


    curr_epoch_loss_val = 0.0
    model = model.eval()
    for i, (features, views) in enumerate(test_loader):
        # Move tensors to the configured device
        with torch.no_grad():
            features = features.to(device).float()
            views = views.to(device).float()
            outputs = model(features).reshape((-1))
            loss = criterion(outputs, views)
            curr_epoch_loss_val+=loss.data.item()
    curr_epoch_loss_val /= len(test)
    loss_list_val.append(curr_epoch_loss_val)
    
    print (f'Epoch [{epoch+1}/{num_epochs}], Total TRAIN epoch Loss: {curr_epoch_loss:.4f}, VAL epoch Loss: {curr_epoch_loss_val:.4f}')




plt.plot(loss_list_train, label = "train_epoch_loss")
plt.plot(loss_list_val, label = "validation_epoch_loss")
plt.ylabel("losses")
plt.xlabel("epoch")
plt.ylim([0,0.05])
plt.legend(loc="upper right")
plt.title(f"{exp_type}")
plt.savefig(f"losses_NN_{exp_type}.png", bbox_inches="tight")