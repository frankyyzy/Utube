import requests
import sys
import json
import pandas as pd
import re
import numpy as np

with open('api_key.txt', 'r') as file:
    api_key = file.readline()


def get_length(video_id):

    searchUrl = "https://www.googleapis.com/youtube/v3/videos?id=" + \
        video_id+"&key="+api_key+"&part=contentDetails"

    request = requests.get(searchUrl)
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()

    data = request.json()
    if 'items' not in data:
        print(data)
        return "Error"
    return data['items'][0]['contentDetails']['duration']


US_videos = pd.read_csv('length.csv')
row = US_videos.shape[0]
hour = np.repeat(-1, row)
min = np.repeat(-1, row)
sec = np.repeat(-1, row)

# -1 not scraped, 0 0 0 means not available
# US_videos['hour'] = hour
# US_videos['min'] = min
# US_videos['sec'] = sec

unavailable_count = 0

dailyNum = 1000
startIndex = 0
first = True

# find start Index

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

for i, r in US_videos[startIndex: startIndex + dailyNum].iterrows():

    curr_id = r['video_id']

    # some videos are unavailable such as: n30k5CwLhS4
    try:
        length = get_length(curr_id)

        if length == 'Error':
            print('stopping at: ', i)
            break

        result = re.search('PT(.*)H(.*)M(.*)S', length)

        if result is not None:
            hour[i] = result.group(1)
            min[i] = result.group(2)
            sec[i] = result.group(3)

        else:
            result = re.search('PT(.*)M(.*)S', length)

            # may have  only seconds or only minutes instead of M and S
            if result is not None:
                currmin = result.group(1)
                currsec = result.group(2)
                hour[i] = 0
                min[i] = currmin
                sec[i] = currsec
            else:
                result = re.search('PT(.*)S', length)

                if result is not None:
                    hour[i] = 0
                    min[i] = 0
                    sec[i] = result.group(1)
                else:
                    result = re.search('PT(.*)M', length)
                    if result is not None:
                        hour[i] = 0
                        min[i] = result.group(1)
                        sec[i] = 0
                    else:
                        print(length)

    except IndexError:
        hour[i] = 0
        min[i] = 0
        sec[i] = 0
        unavailable_count += 1


print('unavailable videos', unavailable_count)

US_videos['hour'] = hour
US_videos['min'] = min
US_videos['sec'] = sec
print(US_videos[startIndex + dailyNum - 5:startIndex + dailyNum + 5])
US_videos.to_csv(r'length.csv', index=False)
# with open('length.csv', 'w') as file:
#     for row in US_videos:
#         file.write(f"{row}\n")
