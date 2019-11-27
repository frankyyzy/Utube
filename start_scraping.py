import requests
import sys
import json
import pandas as pd
import numpy as np

US_videos = pd.read_csv('./youtube-new/INvideos.csv')
row = US_videos.shape[0]
hour = np.repeat(-1, row)
min = np.repeat(-1, row)
sec = np.repeat(-1, row)

# -1 not scraped, 0 0 0 means not available
US_videos['hour'] = hour
US_videos['min'] = min
US_videos['sec'] = sec

US_videos.to_csv(r'length.csv', index=False, line_terminator='\r\n')
