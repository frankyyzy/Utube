import pandas as pd
import numpy as np
import sys

US_videos = pd.read_csv('./length.csv')


row = US_videos.shape[0]
hour = np.repeat(-1, row)
min = np.repeat(-1, row)
sec = np.repeat(-1, row)


def check_all_zero(hour, min, sec):
    return hour == 0 and min == 0 and sec == 0


# for i in range(0, row):
#     notscrape = True
#     for j in range(10):
#         if not check_all_zero(US_videos['hour'][i+j], US_videos['min'][i+j], US_videos['sec'][i+j]):
#             notscrape = False
#     if notscrape:
#         print(i)
#         break

for i, r in US_videos[20698:].iterrows():
    # r['hour'] = -1
    # r['min'] = -1
    # r['sec'] = -1
    US_videos['hour'][i] = -1
    US_videos['min'][i] = -1
    US_videos['sec'][i] = -1

print(US_videos[20690:20700])
# # startIndex = 0
# print(startIndex)


# for i in range(startIndex, 11523):
#     # for i in range(100):
#     curr_id = US_videos['video_id'][i]
#     index = -1
#     for j in range(20000):
#         if US_videos_length['video_id'][j] == curr_id:
#             index = j
#             break
#     if(index != -1):
#         hour[i] = US_videos_length['hour'][index]
#         min[i] = US_videos_length['min'][index]
#         sec[i] = US_videos_length['sec'][index]
#     if (i % 1000 == 0):
#         print(i)
#         US_videos['hour'] = hour
#         US_videos['min'] = min
#         US_videos['sec'] = sec
#         US_videos.to_csv(r'testlength.csv', index=False,
#                          line_terminator='\r\n')

# US_videos['hour'] = hour
# US_videos['min'] = min
# US_videos['sec'] = sec

US_videos.to_csv(r'length.csv', index=False, line_terminator='\r\n')
