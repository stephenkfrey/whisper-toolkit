# Whisper toolkit

# Youtube Transcription 
## --- How to use --- 

Export notebook as `transcribe_youtube.py`, then import to use the key functions



#### example usage 

In your Python script/notebook: 

```
from transcribe_youtube import get_transcription_from_youtube_url, get_transcriptions_from_youtube_playlist

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL9zq2zalZB1JRZsPtYeFVQAZkrDbZx3Qw" # My Learning Playlist 
TEST_URL = "https://www.youtube.com/watch?v=vaUy6zyJfwU" # 1 minute video 

# get transcription for a single video 
single_video_transcription = get_transcription_from_youtube_url(TEST_URL)

# get transcriptions for all videos in a playlist
playlist_transcriptions = get_transcriptions_from_youtube_playlist(PLAYLIST_URL)

```


#### return object
Returns a dict with `title`, `url`, and `transcription`


## Transcribe a video
```
{'title': 'Deep Learning Maps Animal Movement',
 'url': 'https://www.youtube.com/watch?v=vaUy6zyJfwU',
 'transcription': ' We developed a new type of 3D deep learning approach that can take in normal color videos of behaving animals and behaving humans and then output the precise 3D locations of body landmarks so skeletal joints that you can track over time and thus provide a comprehensive description of how subjects are moving. This is a huge leap forward compared to a traditional motion capture system in which subjects need to wear highly invasive markers on the body. And then another big issue with motion captures that it requires that you have a clear line of sights to these markers and in a deep learning-based approach that we develop, we relieve this requirement.'}
 ```

