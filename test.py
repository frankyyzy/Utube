import pandas as pd

# US_videos = pd.read_csv('./youtube-new/USvideos.csv')
# US_videos.to_csv(r'testlength.csv', index=False, line_terminator='\r\n')

US_videos = pd.read_csv('./length.csv')
for i in range(US_videos.shape[0]):
    if (len(US_videos['video_id'][i]) != 11):
        print(i)
        print(US_videos['description'][i - 1])
        print(US_videos['video_id'][i])

print(US_videos['video_id'].str.len().unique())
print(US_videos['video_id'].shape)
