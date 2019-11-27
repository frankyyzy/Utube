import pandas as pd
import numpy as np
import sys

US_videos = pd.read_csv('./testlength.csv')
US_videos_length = pd.read_csv('./length.csv')


row = US_videos.shape[0]
hour = np.repeat(-1, row)
min = np.repeat(-1, row)
sec = np.repeat(-1, row)

for i, r in US_videos.iterrows():

    if r['hour'] == -1:
        startIndex = i
        break
    else:
        hour[i] = r['hour']
        min[i] = r['min']
        sec[i] = r['sec']


# startIndex = 0
print(startIndex)


for i in range(startIndex, 11523):
    # for i in range(100):
    curr_id = US_videos['video_id'][i]
    index = -1
    for j in range(20000):
        if US_videos_length['video_id'][j] == curr_id:
            index = j
            break
    if(index != -1):
        hour[i] = US_videos_length['hour'][index]
        min[i] = US_videos_length['min'][index]
        sec[i] = US_videos_length['sec'][index]
    if (i % 1000 == 0):
        print(i)
        US_videos['hour'] = hour
        US_videos['min'] = min
        US_videos['sec'] = sec
        US_videos.to_csv(r'testlength.csv', index=False,
                         line_terminator='\r\n')

US_videos['hour'] = hour
US_videos['min'] = min
US_videos['sec'] = sec

US_videos.to_csv(r'testlength.csv', index=False, line_terminator='\r\n')
